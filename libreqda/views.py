# -*- coding: utf-8 -*-
import json

from os.path import splitext
from datetime import datetime

from django.http import Http404, HttpResponse
from django.template import RequestContext
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

import libreqda.text_extraction

from libreqda.forms import AddCodeToAnnotation, AddUserToProjectForm,\
    AnnotationForm, BooleanQueryForm, CodeForm, ProjectForm, SetQueryForm,\
    UploadDocumentForm
from libreqda.models import Annotation, BooleanQuery, Code, Document,\
    DocumentInstance, Project, SetQuery, UserProjectPermission


@login_required
def home(request):
    return redirect('browse_projects')


@login_required
def browse_projects(request, template='browse_projects.html'):
    user = request.user
    user_perms = UserProjectPermission.objects.filter(user=user)
    projects = Project.objects.filter(permissions__in=user_perms)

    return render(request, template, {'projects': projects})


@login_required
def new_project(request, template='new_project.html'):
    if request.method == 'POST':
        p = Project()
        form = ProjectForm(request.POST, instance=p)

        if form.is_valid():
            # Create project and set owner
            p.owner = request.user
            p.save()

            # Create an administrative privilege and assign it
            perm = UserProjectPermission()
            perm.creation_date = datetime.now()
            perm.modified_date = datetime.now()
            perm.user = p.owner
            perm.project = p
            perm.permissions = 'a' # admin
            perm.save()

            return redirect('browse_projects')
    else:
        form = ProjectForm()

    form_action = reverse('new_project')
    return render(request,
                  template,
                  {'project_form': form,
                   'form_action': form_action,
                   'back_url': reverse('browse_projects')})


@login_required
def add_user_to_project(request, pid, template='modal.html'):
    if request.method == 'POST':
        form = AddUserToProjectForm(request.POST)
        p = get_object_or_404(Project, pk=pid)

        if form.is_valid():
            for u in form.cleaned_data['users']:
                perm = UserProjectPermission()
                perm.user = u
                perm.project = p
                perm.permissions = 'g'
                perm.save()

            # All OK, redirect to projects home
            response_data = {'redirect': reverse('browse_projects')}
            return HttpResponse(
                        json.dumps(response_data),
                        content_type="application/json")
    else:
        p = get_object_or_404(Project, pk=pid)
        form = AddUserToProjectForm()

    form_action = reverse('add_user_to_project', kwargs={'pid': pid})
    form.fields['users'].queryset = User.objects.exclude(
                                        permissions__in=p.permissions.all())
    response_dict = {
                     'form': form,
                     'form_action': form_action,
                     'form_header': _('Asignar usuarios al proyecto'),
                    }
    html_response = render_to_string(
                        template, response_dict, RequestContext(request))

    response_data = {'html': html_response}
    return HttpResponse(
                json.dumps(response_data),
                content_type="application/json")


@login_required
def remove_user_from_project(request, pid, uid):
    p = get_object_or_404(Project, pk=pid)
    u = get_object_or_404(User, pk=uid)
    admin_perm = UserProjectPermission.objects.filter(
                        user=request.user, project=p, permissions='a')

    if u == p.owner:
        raise Exception(_('No se puede remover del projecto a su propietario.'))

    if p.owner == request.user or admin_perm.exists():
        perm = UserProjectPermission.objects.get(user=u, project=p)
        perm.delete()
    else:
        raise Exception(_('Permisos insuficientes.'))

    return redirect('browse_projects')


@login_required
def delete_project(request, pid):
    p = get_object_or_404(Project, pk=pid)
    if p.owner == request.user:
        p.delete()
    else:
        raise Http404

    return redirect('browse_projects')


@login_required
def copy_project(request, pid, template='copy_project.html'):
    p = get_object_or_404(Project, pk=pid)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=p)

        if form.is_valid():
            p.owner = request.user
            p.pk = None
            p.save()

            return redirect('browse_projects')
    else:
        form = ProjectForm()

    form_action = reverse('copy_project',
                          args=(pid,))
    return render(request,
                  template,
                  {'project_form': form,
                   'form_action': form_action,
                   'back_url': reverse('browse_projects')})


@login_required
def view_document(request, pid, did, template='view_document.html'):
    p = get_object_or_404(Project, pk=pid)
    d = get_object_or_404(DocumentInstance, pk=did)

    return render(request,
                  template,
                  {'project': p,
                   'document': d})


#Uncomment this to enable file selection instead of uploading a new file
#@login_required
#def new_document(request, pid, template='new_document.html'):
#    p = get_object_or_404(Project, pk=pid)
#
#    if request.method == 'POST':
#        form = NewDocumentForm(request.POST)
#        if form.is_valid():
#            name = form.cleaned_data['name']
#            comment = form.cleaned_data['comment']
#            document_id = form.cleaned_data['document']
#            document = get_object_or_404(Document, pk=document_id)
#
#            doc_instance = DocumentInstance(name=name,
#                                            project=p,
#                                            comment=comment,
#                                            document=document,
#                                            type=document.type,
#                                            uploaded_by=request.user)
#            doc_instance.save()
#            return redirect('browse_projects')
#    else:
#        form = NewDocumentForm()
#
#    return render(request,
#              template,
#              {'project': p,
#               'documents': Document.objects.all(),
#               'form': form})


def extract_text(path, extension):
    return getattr(libreqda.text_extraction, extension.lower()[1:])(path)


@login_required
def upload_document(request, pid, template='upload_document.html'):
    p = get_object_or_404(Project, pk=pid)

    if request.method == 'POST':
        form = UploadDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            comment = form.cleaned_data['comment']
            document_file = request.FILES['document']
            document = Document(name=name,
                                comment=comment,
                                uploaded_by=request.user,
                                file=document_file,
                                type=splitext(document_file.name)[1])
            document.save()

            doc_instance = DocumentInstance(name=name,
                                            project=p,
                                            comment=comment,
                                            document=document,
                                            type=document.type,
                                            uploaded_by=request.user)
            doc_instance.save()
            document.file.close()

            try:
                text = extract_text(document.file.name,
                                    document.type)
                document.text = text
                document.save()
                doc_instance.save()
            except:
                doc_instance.delete()
                document.file.delete()
                document.delete()

            return redirect('browse_projects')
    else:
        form = UploadDocumentForm()

    back_url = reverse('browse_projects')
    form_action = reverse('upload_document', args=(pid,))
    return render(request,
              template,
              {'project': p,
               'documents': Document.objects.all(),
               'form': form,
               'form_action': form_action,
               'back_url': back_url})


@login_required
def delete_document(request, pid, did):
    p = get_object_or_404(Project, pk=pid)
    d = get_object_or_404(DocumentInstance, pk=did)

    if p.owner == request.user:
        d.document.delete()
        d.delete()
    else:
        raise Http404

    return redirect('browse_projects')


@login_required
def browse_codes(request, pid, template='browse_codes.html'):
    p = get_object_or_404(Project, pk=pid)

    return render(request,
              template,
              {'project': p})


@login_required
def new_code(request, pid, template='new_code.html'):
    p = get_object_or_404(Project, pk=pid)

    back_or_success = reverse('browse_codes', args=(pid,))

    if request.method == 'POST':
        c = Code()
        form = CodeForm(request.POST, instance=c)
        if form.is_valid():
            c.created_by = request.user
            c.project = p
            c.save()

            return redirect(back_or_success)
    else:
        form = CodeForm()

    form_action = reverse('new_code', args=(pid,))
    return render(request,
              template,
              {'form': form,
               'form_action': form_action,
               'back_url': back_or_success})


@login_required
def delete_code(request, pid, cid):
    p = get_object_or_404(Project, pk=pid)
    c = get_object_or_404(Code, pk=cid)

    if c.project == p and c.created_by == request.user:
        c.delete()
    else:
        raise Http404

    return redirect('browse_codes', pid=pid)


@login_required
def browse_annotations(request, pid, template='browse_annotations.html'):
    p = get_object_or_404(Project, pk=pid)

    return render(request,
              template,
              {'project': p})


@login_required
def new_annotation(request, pid, template='new_annotation.html'):
    p = get_object_or_404(Project, pk=pid)

    back_or_success = reverse('browse_annotations', args=(pid,))

    if request.method == 'POST':
        a = Annotation()
        form = AnnotationForm(request.POST, instance=a)
        if form.is_valid():
            a.created_by = request.user
            a.project = p
            a.save()

            return redirect(back_or_success)
    else:
        form = AnnotationForm()

    form_action = reverse('new_annotation', args=(pid,))
    return render(request,
              template,
              {'form': form,
               'form_action': form_action,
               'back_url': back_or_success})


@login_required
def delete_annotation(request, pid, aid):
    p = get_object_or_404(Project, pk=pid)
    a = get_object_or_404(Annotation, pk=pid)

    if request.user in p.admin_users():
        a.delete()
    else:
        raise Http404

    return reverse('browse_annotations', args=(pid,))


@login_required
def add_code_to_annotation(request, pid, aid, template='modal.html'):
    p = get_object_or_404(Project, pk=pid)
    a = get_object_or_404(Annotation, pk=aid)

    if a.project != p:
        raise Http404

    if request.method == 'POST':
        form = AddCodeToAnnotation(request.POST)
        form.fields['codes'].queryset = p.codes.all()

        if form.is_valid():
            for code in form.cleaned_data['codes']:
                a.codes.add(code)
            a.save()

            response_data = {'redirect': reverse('browse_annotations',
                                                 args=(pid,))}
            return HttpResponse(json.dumps(response_data),
                                content_type="application/json")
    else:
        form = AddCodeToAnnotation()

    form_action = reverse('add_code_to_annotation', args=(pid, aid))
    form.fields['codes'].queryset = p.codes.exclude(id__in=a.codes.all().values('id'))

    response_dict = {
                     'form': form,
                     'form_action': form_action,
                     'form_header': _('Asignar códigos a la anotación'),
                    }
    html_response = render_to_string(
                        template, response_dict, RequestContext(request))

    response_data = {'html': html_response}
    return HttpResponse(
                json.dumps(response_data),
                content_type="application/json")


@login_required
def remove_code_from_annotation(request, pid, aid, cid):
    p = get_object_or_404(Project, pk=pid)
    a = get_object_or_404(Annotation, pk=aid)
    c = get_object_or_404(Code, pk=cid)

    if c not in a.codes.all():
        raise Http404

    if request.user in p.admin_users():
        a.codes.remove(c)
        a.save()
    else:
        raise Http404

    return redirect('browse_annotations', pid=pid)


@login_required
def browse_queries(request, pid, template='browse_queries.html'):
    p = get_object_or_404(Project, pk=pid)

    return render(request, template, {'project': p})


@login_required
def new_boolean_query(request, pid, template='new_boolean_query.html'):
    p = get_object_or_404(Project, pk=pid)

    if request.user not in p.admin_users():
        raise Http404

    back_or_success = reverse('browse_queries', args=(pid,))

    if request.method == 'POST':
        b = BooleanQuery()
        form = BooleanQueryForm(request.POST, instance=b)
        form.fields['codes'].queryset = p.codes.all()

        if form.is_valid():
            b.project = p
            b.save()

            for code in form.cleaned_data['codes']:
                b.codes.add(code)
            b.save()

            return redirect('browse_queries', pid=pid)
    else:
        form = BooleanQueryForm()
        form.fields['codes'].queryset = p.codes.all()

    form_action = reverse('new_boolean_query', args=(pid,))

    return render(request,
                  template,
                  {'form': form,
                   'form_action': form_action,
                   'back_url': back_or_success})


@login_required
def delete_boolean_query(request, pid, qid):
    p = get_object_or_404(Project, pk=pid)
    q = get_object_or_404(BooleanQuery, pk=qid)

    if q.project != p:
        raise Http404

    if request.user not in p.admin_users():
        raise Http404

    for qq in q.containing_queries.all():
        qq.delete()
    q.delete()

    return redirect('browse_queries', pid=pid)


@login_required
def new_set_query(request, pid, template='new_set_query.html'):
    p = get_object_or_404(Project, pk=pid)

    if request.user not in p.admin_users():
        raise Http404

    back_or_success = reverse('browse_queries', args=(pid,))

    if request.method == 'POST':
        s = SetQuery()
        form = SetQueryForm(request.POST, instance=s)
        form.fields['queries'].queryset = p.boolean_queries.all()

        if form.is_valid():
            s.project = p
            s.save()

            for q in form.cleaned_data['queries']:
                s.queries.add(q)
            s.save()

            return redirect('browse_queries', pid=pid)
    else:
        form = SetQueryForm()
        form.fields['queries'].queryset = p.boolean_queries.all()

    form_action = reverse('new_set_query', args=(pid,))

    return render(request,
                  template,
                  {'form': form,
                   'form_action': form_action,
                   'back_url': back_or_success})


@login_required
def delete_set_query(request, pid, qid):
    p = get_object_or_404(Project, pk=pid)
    q = get_object_or_404(SetQuery, pk=qid)

    if q.project != p:
        raise Http404

    if request.user not in p.admin_users():
        raise Http404

    q.delete()

    return redirect('browse_queries', pid=pid)


def __do_query(request, pid, qid, t, template='browse_query_results.html'):
    p = get_object_or_404(Project, pk=pid)
    query = get_object_or_404(t, pk=qid)

    if query.project != p:
        raise Http404

    citations = query.execute()
    results = {}

    for c in citations:
        for code in c.codes.all():
            if code in results:
                results[code.id]['citations'].append(c)
            else:
                results[code.id] = {'id': code.id,
                                    'name': code.name,
                                    'citations': [c]}

    res = results.values()
    return render(request,
                  template,
                  {'project': p,
                   'results': res})


@login_required
def do_boolean_query(request, pid, qid):
    return __do_query(request, pid, qid, BooleanQuery)


@login_required
def do_set_query(request, pid, qid):
    return __do_query(request, pid, qid, SetQuery)

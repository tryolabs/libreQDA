from datetime import datetime

from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from libreqda.forms import ProjectForm, AddUserToProjectForm
from libreqda.models import Document, Project, UserProjectPermission


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
                perm.creation_date = datetime.now()
                perm.modified_date = datetime.now()
                perm.user = u
                perm.project = p
                perm.permissions = 'g'
                perm.save()
            return redirect('browse_projects')
    else:
        p = get_object_or_404(Project, pk=pid)
        form = AddUserToProjectForm()
        existing_perms = UserProjectPermission.objects.filter(project=p)
        form.fields['users'].queryset = User.objects.exclude(
                                            permissions__in=existing_perms
                                            ).exclude(pk=p.owner.pk)

    form_action = reverse('add_user_to_project', kwargs={'pid': pid})
    return render(request,
                  template,
                  {'form': form,
                   'form_action': form_action,
                   'form_header': 'Asignar usuarios al proyecto',
                   'back_url': reverse('browse_projects')})


@login_required
def remove_user_from_project(request, pid, uid):
    p = get_object_or_404(Project, pk=pid)
    u = get_object_or_404(User, pk=uid)
    admin_perm = UserProjectPermission.objects.filter(
                        user=request.user, project=p, permissions='a')

    if u == p.owner:
        raise Exception('No se puede remover del projecto a su propietario.')

    if p.owner == request.user or admin_perm.exists():
        perm = UserProjectPermission.objects.get(user=u, project=p)
        perm.delete()
    else:
        raise Exception('Permisos insuficientes.')

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
    d = get_object_or_404(Document, pk=did)

    return render(request,
                  template,
                  {'project': p,
                   'document': d})

# -*- coding: utf-8 -*-

import re
from datetime import datetime

from django.http import HttpResponse
from django.utils import simplejson as json
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from libreqda.utils import JsonResponse
from libreqda.models import DocumentInstance, Citation


###TODO:Resolver temas de permisos en todas las vistas.

@csrf_exempt #TODO: Fix this to include csrf token in Annotations post
@login_required
def create(request, pid, did):
    try:
        serialized_annotation = request.POST.keys()[0]
    except IndexError:
        raise Exception("Invalid annotation data in 'create'")

    user = request.user
    doc = get_object_or_404(DocumentInstance, pk=did)
    c = populate_citation(Citation(), serialized_annotation, doc, user)

    return HttpResponse(c.serialized,
                        mimetype='application/json; charset=utf8')

@login_required
def read(request, pid, did, aid=None):
    doc = get_object_or_404(DocumentInstance, pk=did)

    citations = [cit.serialized for cit in doc.citations.all()]
    if not citations:
        return JsonResponse([])

    content = '[%s]' % (','.join(citations),)
    return HttpResponse(content, mimetype='application/json; charset=utf8')

@csrf_exempt #TODO: Fix this to include csrf token in Annotations post
@login_required
def update(request, pid, did, aid):
    user = request.user
    doc = get_object_or_404(DocumentInstance, pk=did)
    citation = doc.citations.get(pk=aid)

    serialized_annotation = request.body
    citation = populate_citation(citation, serialized_annotation,
                                 doc, user, citation_id=aid)

    return HttpResponse(citation.serialized,
                        mimetype='application/json; charset=utf8')

@csrf_exempt #TODO: Fix this to include csrf token in Annotations post
@login_required
def destroy(request, pid, did, aid):
    doc = get_object_or_404(DocumentInstance, pk=did)
    citation = doc.citations.get(pk=aid)
    citation.delete()

    return JsonResponse('', status=204)

#### Helper functions for annotations views

def populate_citation(citation, serialized_annotation,
                        document, user, citation_id=None):
    '''
    Populates a freshly created Citation object or updates an
    already created one from a serialized annotation.
    
    Returns the citation with updated fields.
    '''

    c = citation
    annotation = json.loads(serialized_annotation)

    c.created_by = user
    c.document = document
    c.comment = annotation['text']

    a_range = get_range_from_annotation(annotation['ranges'][0])
    c.start_paragraph = a_range['start_p']
    c.end_paragraph = a_range['end_p']
    c.start = a_range['start']
    c.end = a_range['end']

    if not citation_id:
        # Freshly created citation.
        c.creation_date = datetime.now()
        c.modified_date = c.creation_date
        c.serialized = serialized_annotation
        c.save()

        annotation['id'] = c.id
        c.serialized = json.dumps(annotation)
        c.save()
    else:
        annotation['id'] = citation_id
        c.serialized = json.dumps(annotation)
        c.modified_date = datetime.now()
        c.save()

    return c

def get_range_from_annotation(range_dict):
    '''
    Given an annotation range dictionary it returns a dic with
    the following keys:
        start_p : Start paragraph, end_p : End paragraph,
        start : Start offset in paragraph, end : End offset in paragraph
    '''
    range_RE = r'/p\[(\d+)\]'

    start = range_dict['startOffset']
    end = range_dict['endOffset']
    start_p = re.findall(range_RE, range_dict['start'])[0]
    end_p = re.findall(range_RE, range_dict['end'])[0]

    return {
        'start_p'   : int(start_p),
        'end_p'     : int(end_p),
        'start'     : start,
        'end'       : end,
    }

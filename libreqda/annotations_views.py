import re
from datetime import datetime

from django.http import HttpResponse
from django.utils import simplejson as json
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from libreqda.utils import JsonResponse
from libreqda.models import DocumentInstance, Citation


@csrf_exempt #TODO: Fix this to include csrf token in Annotations post
@login_required
def create(request, pid, did):
    try:
        print request.POST.keys()
        serialized_annotation = request.POST.keys()[0]
    except IndexError:
        raise Exception("Invalid annotation data in 'create'")

    user = request.user
    doc = get_object_or_404(DocumentInstance, pk=did)
    annotation = json.loads(serialized_annotation)

    c = Citation()
    c.document = doc
    c.created_by = user
    c.creation_date = datetime.now()
    c.modified_date = c.creation_date

    a_range = get_range_from_annotation(annotation['ranges'][0])
    c.start_paragraph = a_range['start_p']
    c.end_paragraph = a_range['end_p']
    c.start = a_range['start']
    c.end = a_range['end']

    c.comment = annotation['text']
    c.serialized = serialized_annotation
    c.save()

    return JsonResponse('OK')

@login_required
def read(request, pid, did, aid=None):
    doc = get_object_or_404(DocumentInstance, pk=did)

    citations = [cit.serialized for cit in doc.citations.all()]
    if not citations:
        return JsonResponse([])

    content = '[%s]' % (','.join(citations),)
    return HttpResponse(content, mimetype='application/json; charset=utf8')


#### Helper functions for annotations views

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

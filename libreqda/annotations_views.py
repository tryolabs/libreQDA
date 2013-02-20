import re
from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils import simplejson as json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from libreqda.utils import JsonResponse
from libreqda.models import DocumentInstance, Citation

@login_required
def base(request):
    return redirect('browse_projects')


@csrf_exempt #TODO: Fix this to include csrf token in Annotations post
@login_required
def create(request):
    try:
        print request.POST.keys()
        serialized_annotation = request.POST.keys()[0]
    except IndexError:
        raise Exception("Invalid annotation data in 'create'")

    annotation = json.loads(serialized_annotation)
    user = request.user
    doc = DocumentInstance.objects.get(pk=1) #TODO: just for testing, fix

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
def read(request, aid=None):
    doc = DocumentInstance.objects.get(pk=1) #TODO: just for testing, fix

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

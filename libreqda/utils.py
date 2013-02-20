from django.http import HttpResponse
from django.utils import simplejson

class JsonResponse(HttpResponse):
    def __init__(self, data):
        content = simplejson.dumps(
                    data,
                    indent=2,
                    ensure_ascii=False)
        super(JsonResponse, self).__init__(
                                    content=content,
                                    mimetype='application/json; charset=utf8')

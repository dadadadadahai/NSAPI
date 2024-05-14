from django.http import HttpResponse
import json
# Create your views here.
def get(request):
     print(json.dumps(request.GET))
     return HttpResponse('ok')
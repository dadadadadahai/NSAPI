from django.http import HttpResponse
from django.conf import settings
import requests,logging
url = 'http://190.92.241.159:9090/sms/batch/v2'
# Create your views here.
def send(request,code,phone):
    return twoBx(code,phone)


def twoBx(code,phone):
    phone = '55'+phone
    formdata = {}
    url='http://api.wftqm.com/api/sms/mtsend'
    formdata['appkey'] ='TP2ZwR19'
    formdata['secretkey']='OeGWopNp'
    formdata['phone'] = phone
    formdata['content'] =code + ' é o seu codigo de verifica {o, válido por dez minutos'
    res=requests.post(url,data=formdata,headers={'Content-Type':'application/x-www-form-urlencoded'})
    return HttpResponse('SUCCESS')


def oneBx(code,phone):
    phone = '55' + phone
    request = {}
    request['appkey'] = settings.SMS01['appkey']
    request['appsecret'] = settings.SMS01['appsecret']
    request['phone'] = phone
    request['msg'] = code + ' é o seu codigo de verifica {o, válido por dez minutos'
    querystr = url + '?'
    for key in request:
        querystr = querystr + '{}={}&'.format(key, request[key])
    querystr = querystr[:len(querystr) - 1]
    response = requests.get(querystr)
    jsonobj = response.json()
    if jsonobj['code'] == '00000':
        return HttpResponse('SUCCESS')
    else:
        logging.error('短信发送接口-{}'.format(response.json()))
        return HttpResponse('Fail')

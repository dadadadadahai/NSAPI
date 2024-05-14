from django.http import HttpResponse,JsonResponse
import requests
import json
from django.conf import settings
from .models import userinfo,adidlog,mechineArray
import IPy
Allow = True
WriteIpArray=['124.248.219.141']
CNIPS=[]
# Create your views here.
def addMechine(request,mechine):
    mechineArray(_id=mechine).save()
    return HttpResponse('OK')
def isReport(request):
    if request.method == 'POST':
        postBody = request.body
        jsonobj = json.loads(postBody)
        adid = jsonobj['adid']
        uinfo = adidlog.objects(_id=adid).first()
        if uinfo is None:
            adidlog(_id=adid,postData=postBody,openView=jsonobj['openView']).save()
            return HttpResponse('true')
        else:
            return HttpResponse('false')

def queryUidByAdid(request,adid):
    uinfo = userinfo.objects(base__adjustId=adid).first()
    if uinfo is None:
        return  HttpResponse('None')
    else:
        return  HttpResponse(uinfo._id)
#

#获取IP地址
def get(request,mechine):
    uinfo = userinfo.objects(base__adjustId=mechine).first()
    if uinfo and uinfo.base.regFlag==1:
        return HttpResponse('B')
    mechineinfo =mechineArray.objects(_id=mechine).first()
    if mechineinfo:
        return HttpResponse('B')
    forwarded_addresses = request.META.get('HTTP_X_FORWARDED_FOR')
    if forwarded_addresses:
        client_addr = forwarded_addresses.split(',')[0]
    else:
        client_addr = request.META.get('REMOTE_ADDR')
    if client_addr in WriteIpArray:
        return HttpResponse('B')
    if Allow:
        return HttpResponse('A')
    headers={
        'Fastah-Key':'a716dd132acc4eb89eca9c727f60cdc2'
    }
    response = requests.get('https://ep.api.getfastah.com/whereis/v1/json/'+client_addr,headers=headers)
    rp = response.json()
    if rp['locationData']['countryName']=='Brazil':
        return HttpResponse('B')
    else:
        return HttpResponse('A')

def get1(request):
    forwarded_addresses = request.META.get('HTTP_X_FORWARDED_FOR')
    if forwarded_addresses:
        client_addr = forwarded_addresses.split(',')[0]
    else:
        client_addr = request.META.get('REMOTE_ADDR')
    if client_addr in WriteIpArray:
        return HttpResponse('B')
    if Allow:
        return HttpResponse('A')
    headers={
        'Fastah-Key':'a716dd132acc4eb89eca9c727f60cdc2'
    }
    response = requests.get('https://ep.api.getfastah.com/whereis/v1/json/'+client_addr,headers=headers)
    rp = response.json()
    if rp['locationData']['countryName']=='Brazil':
        return HttpResponse('B')
    else:
        return HttpResponse('A')
#是否跳转
def IsRedJump(request):
    ip = IPy.IP(getRemoteIp(request))
    for ips in CNIPS:
        cnIp = IPy.IP(ips)
        if ip in cnIp:
            return JsonResponse({
                'url':settings.JUMP_404
            })
    return JsonResponse({
        'url':''
    })
#读取ip配置
def readIpZoneCfg():
    with open('cnIp.txt','r') as f:
        line = f.readline()
        while line:
            CNIPS.append(line)
            line = f.readline()
def getRemoteIp(request):
    if request.environ.get("HTTP_X_REAL_IP", False):
        # 从环境信息获取
        ip = request.environ.get("HTTP_X_REAL_IP", None)
    elif request.headers.get("X-Real-Ip", False):
        # 从头部信息获取
        ip = request.headers.get("X-Real-Ip", None)
    else:
        # 获取一般的地址
        ip = request.META['REMOTE_ADDR']
    return ip


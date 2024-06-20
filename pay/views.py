from django.shortcuts import render
from django.http import JsonResponse
from errorDefine import errorDefine
from django.conf import settings
from . import models,payTest,FastPay,Goopagoo,hkpPay,SitoBank
from . import Tools
import random
# Create your views here.
#发起支付请求
def payrequest(request,uid,shopId,price,channelNo,paytype):
    ip = Tools.getRemoteIp(request)
    fbp = request.GET.get('fbp',default='')
    fbc = request.GET.get('fbc',default='')
    click_id = request.GET.get('click_id',default='')
    uinfo = models.userinfo.objects(_id=uid).first()
    if not uinfo:
        return JsonResponse({'errno':errorDefine.NOUSER})
    if price<=0:
        return JsonResponse({'errno':errorDefine.MONEYERROR})
    host = request.META['HTTP_HOST']
    index = host.index(':')
    host ='https://' + host[:index]
    channelinfo={
        "ip":ip,
        "fbp":fbp,
        "fbc":fbc,
        'HTTP_HOST':host
    }
    rand = random.randint(1,100)
    # if channelNo==6 or channelNo==4:
    #     if rand<=70:
    #         channelNo=3
    #进入支付,发起
    if channelNo==3:
        rdata = FastPay.RequestPay(uid,shopId,price,uinfo,click_id,channelinfo,paytype)
    elif channelNo==4:
        rdata = Goopagoo.RequestPay(uid,shopId,price,uinfo,click_id,channelinfo)
    elif channelNo==5:
        rdata = SitoBank.RequestPay(uid,shopId,price,uinfo,click_id,channelinfo)
    elif channelNo == 6:
        rdata = hkpPay.RequestPay(uid, shopId, price, uinfo, click_id, channelinfo)
    elif channelNo==10:
        rdata = payTest.payTest(uid,shopId,price,paytype)
    return JsonResponse(rdata)

def payrequestUrl(request,uid,shopId,price,channelNo):
    ip = Tools.getRemoteIp(request)
    fbp = request.GET.get('fbp',default='')
    fbc = request.GET.get('fbc',default='')
    click_id = request.GET.get('click_id', default='')
    uinfo = models.userinfo.objects(_id=uid).first()
    if not uinfo:
        return JsonResponse({'errno':errorDefine.NOUSER})
    if price<=0:
        return JsonResponse({'errno':errorDefine.MONEYERROR})
    host = request.META['HTTP_HOST']
    index = host.index(':')
    host ='https://' + host[:index]
    channelinfo={
        "ip":ip,
        "fbp":fbp,
        "fbc":fbc,
        'HTTP_HOST': host
    }
    rand = random.randint(1,100)
    # if channelNo==6 or channelNo==4:
    #     if rand<=70:
    #         channelNo=3
    #进入支付,发起
    if channelNo==3:
        rdata = FastPay.RequestPay(uid,shopId,price,uinfo,click_id,channelinfo)
    elif channelNo==4:
        rdata = Goopagoo.RequestPay(uid,shopId,price,uinfo,click_id,channelinfo)
    elif channelNo == 5:
        rdata = SitoBank.RequestPay(uid, shopId, price, uinfo, click_id, channelinfo)
    elif channelNo==6:
        rdata = hkpPay.RequestPay(uid, shopId, price, uinfo, click_id, channelinfo)
    elif channelNo == 10:
        rdata = payTest.payTest(uid, shopId, price)
    return JsonResponse(rdata)
def testCallBackUp(request):
    host = request.META['HTTP_HOST']
    index = host.index(':')
    host ='https://' + host[:index]
    print(host)
    return JsonResponse({'errno':1})

def kwViewContent(request,uid):
    click_id = request.GET.get('click_id',default='')
    fbc =  request.GET.get('fbc', default='')
    fbp = request.GET.get('fbp',default='')
    pixelvalue = request.GET.get('pixelvalue',default='')
    #直接调用tools
    if click_id!='':
        Tools.viewSuccessCallBackKW(uid,click_id,pixelvalue)
    elif fbp!='' and fbc!='':
        Tools.viewSuccessCallBackFB(uid,fbc,fbp,pixelvalue)
    return JsonResponse({'errno':'success'})

import json

import requests,time,calendar,logging,qrcode,io,base64
from . import models
import logging,psutil,socket
import pandas as pd
from django_redis import get_redis_connection
from django.conf import settings
from requests_toolbelt import SourceAddressAdapter
pixelcfg={}
cfgxls = pd.read_excel('fbpixcode.xlsx')
for item in cfgxls.values:
    pixelcode=str(item[0])
    token = item[3]
    hv =float(item[4])
    http=item[6].split('?')[0]
    if pixelcode!='' and token!='':
        pixelcfg[pixelcode.strip()] = {'token':token.strip(),'hv':hv,'http':http}
def getPushUrl(pixelcode):
    url = 'https://graph.facebook.com/v18.0/%s/events?access_token=%s'
    if pixelcode in pixelcfg:
        url = url % (pixelcode,pixelcfg[pixelcode]['token'])
    return url
def paySuccessCallBackFbTest(price,ip,fbc,fbp,pixelcode,HTTP_HOST):
    if ip=='' or fbc=='' or fbp=='':
        return
    hv = 4.9
    if pixelcode in pixelcfg:
        hv = pixelcfg[pixelcode]['hv']
        HTTP_HOST = pixelcfg[pixelcode]['http']
    price = round(price/100)
    us = round(price/hv,2)
    if HTTP_HOST=='':
        return
    senddata = {
        "data":[
            {
                # "event_name": "first_purchase",
                "event_name": "Purchase",
                "event_time":calendar.timegm(time.gmtime()),
                "user_data": {
                    "client_ip_address":ip,
                    "fbc":fbc,
                    "fbp":fbp
                },
                "custom_data": {
                    "currency": "usd",
                    "value": us,
                },
                "event_source_url": HTTP_HOST,
                "action_source": "website"
            }
        ]
    }
    url = getPushUrl(pixelcode)
    s=requests.session()
    new_source=SourceAddressAdapter(settings.BIND_IP)
    s.mount('http://',new_source)
    s.mount('https://', new_source)
    response = s.post(url=url,json=senddata)
    print(response.text,HTTP_HOST)
def payFBAllTest():
    for key in pixelcfg:
        http = pixelcfg[key]['http']
        if True:
            paySuccessCallBackFbTest(3000, '182.148.13.141 ',
                                 'fb.1.1701328520680.IwAR1NKiVYHmsgJ-bi8KOje3fj9ZJVud2PuU1e3Up1_iYPsdXZDtLWLLmGxGw',
                                 'fb.1.1701156039780.182735580',key,'')

#payFBAllTest()

#FB上报各种数据
def repotFbEvent(pixecode,method,fbc,fbp,ip):
    if pixecode=="" or fbp=="" or fbc=="":
        return
    HTTP_HOST=''
    if pixecode in pixelcfg:
        HTTP_HOST = pixelcfg[pixecode]['http']
    else:
        return
    senddata = {
        "data": [
            {
                # "event_name": "first_purchase",
                "event_name": method,
                "event_time": calendar.timegm(time.gmtime()),
                "user_data": {
                    "client_ip_address": ip,
                    "fbc": fbc,
                    "fbp": fbp
                },
                "custom_data": {
                },
                "event_source_url": HTTP_HOST,
                "action_source": "website"
            }
        ]
    }
    url = getPushUrl(pixelcode)
    s=requests.session()
    new_source=SourceAddressAdapter(settings.BIND_IP)
    s.mount('http://',new_source)
    s.mount('https://', new_source)
    response = s.post(url=url,json=senddata)
    # response = requests.post(url=url, json=senddata)
    print(response.text)
def paySuccessCallBackFirst(uid,price,ip,fbc,fbp,pixelcode,HTTP_HOST,ucinfo):
    if ip=='' or fbc=='' or fbp=='' or ucinfo.IsFirst>0:
        return
    price = round(price/500)
    hv = 4.9
    if pixelcode in pixelcfg:
        hv = pixelcfg[pixelcode]['hv']
        HTTP_HOST = pixelcfg[pixelcode]['http']
    us = round(price/hv,2)
    if HTTP_HOST=='':
        return
    senddata = {
        "data":[
            {
                "event_name": "first_purchase",
                "event_time":calendar.timegm(time.gmtime()),
                "user_data": {
                    "client_ip_address":ip,
                    "fbc":fbc,
                    "fbp":fbp
                },
                "custom_data": {
                    "currency": "usd",
                    "value": us,
                },
                "event_source_url": HTTP_HOST,
                "action_source": "website"
            }
        ]
    }
    url = getPushUrl(pixelcode)
    response = requests.post(url=url,json=senddata)
    logger = logging.getLogger('django')
    logger.info('response=%s,pixelcode=%s first'%(response.text,pixelcode))
    models.uchannelinfo.objects(_id=uid).update(IsFirst=1)
#支付成功后回传fb
def paySuccessCallBackFb(price,ip,fbc,fbp,pixelcode,HTTP_HOST):
    if ip=='' or fbc=='' or fbp=='':
        return
    price = round(price/500)
    hv = 4.9
    if pixelcode in pixelcfg:
        hv = pixelcfg[pixelcode]['hv']
        HTTP_HOST = pixelcfg[pixelcode]['http']
    us = round(price / hv, 2)
    if HTTP_HOST=='':
        return
    senddata = {
        "data":[
            {
                # "event_name": "first_purchase",
                "event_name": "Purchase",
                "event_time":calendar.timegm(time.gmtime()),
                "user_data": {
                    "client_ip_address":ip,
                    "fbc":fbc,
                    "fbp":fbp
                },
                "custom_data": {
                    "currency": "usd",
                    "value": us,
                },
                "event_source_url": HTTP_HOST,
                "action_source": "website"
            }
        ]
    }
    url = getPushUrl(pixelcode)
    s=requests.session()
    new_source=SourceAddressAdapter(settings.BIND_IP)
    s.mount('http://',new_source)
    s.mount('https://', new_source)
    response = s.post(url=url,json=senddata)
    # response = requests.post(url=url,json=senddata)
    print(response.text)
    logger = logging.getLogger('django')
    logger.info('response=%s,pixelcode=%s'%(response.text,pixelcode))
def kwIdToToken(pixelvalue):
    if pixelvalue=='571424621657337921':
        return 'fMWLhiaK28UnTVB4cw+KWajDJ833oqvBisDiG/0dFkw='
    elif pixelvalue=='571413691213033523':
        return 'wDjPb3V/Fkl97vqssDWpIiBue38KRMJ/n+T3vVC7xO0='
    elif pixelvalue=='249700980992654':
        return 'd6FGC3Y1tZcgOW8lLRXgF2i9FkMQqnxrEfuNL0Uuyew='
def paySuccessCallBackKW(price,click_id,shopId,pixelvalue):
    if click_id=='':
        return
    token = kwIdToToken(pixelvalue)
    price = round(price / 500)
    us = round(price / 4.9, 2)
    property="""{"content_id":%d,"value"=%.2f}"""%(shopId,us)
    senddata={
        "access_token":token,
        "clickid":click_id,
        "event_name":"EVENT_PURCHASE",
        "is_attributed":1,
        "mmpcode":"PL",
        "pixelId":pixelvalue,
        "pixelSdkVersion":"9.9.9",
        "properties":property,
        "testFlag":False,
        "third_party":"web",
        "trackFlag":False
    }
    url='http://www.adsnebula.com/log/common/api'
    header={
        "accept":"application/json;charset=utf-8",
        "Content-Type":"application/json"
    }
    s=requests.session()
    new_source=SourceAddressAdapter(settings.BIND_IP)
    s.mount('http://',new_source)
    s.mount('https://', new_source)
    response = s.post(url=url,headers=header,json=senddata)
    # response = requests.post(url=url,headers=header,json=senddata)
    print(response.text)
    logger = logging.getLogger('django')
    logger.info('response=%s,pixelvalue=%s kw' % (response.text, pixelvalue))

# paySuccessCallBackKW(3000,'gZqY4VFFdDONtsepSFXHLgoe98swz3cri7YXGqauzipnsBuckFN_ZJ94x9zTeDRp3JvueqWkRUnu2HyICAgtiRACCPrMffTNI6rqIwb5624=',101,'571424621657337921')

def paySuccessCallBackKWTest(price,click_id,shopId,pixelvalue):
    if click_id=='':
        return
    token = kwIdToToken(pixelvalue)
    price = round(price / 100)
    us = round(price / 4.9, 2)
    property="""{"content_id":%d,"value"=%.2f}"""%(shopId,us)
    senddata={
        "access_token":token,
        "clickid":click_id,
        # "event_name":"EVENT_PURCHASE",
        "event_name": "EVENT_CONTENT_VIEW",
        "is_attributed":1,
        "mmpcode":"PL",
        "pixelId":pixelvalue,
        "pixelSdkVersion":"9.9.9",
        "properties":property,
        "testFlag":False,
        "third_party":"web",
        "trackFlag":True
    }
    url='http://www.adsnebula.com/log/common/api'
    header={
        "accept":"application/json;charset=utf-8",
        "Content-Type":"application/json"
    }
    s=requests.session()
    new_source=SourceAddressAdapter(settings.BIND_IP)
    s.mount('http://',new_source)
    s.mount('https://', new_source)
    response = s.post(url=url,headers=header,json=senddata)
    # response = requests.post(url=url,headers=header,json=senddata)
    print(response.text)
# paySuccessCallBackKWTest(3000,'/Vevh+i6B3scIv8LE9Qv0g==',101,'571424621657337921')

#快手页面被查看事件
def viewSuccessCallBackKW(uid,click_id,pixelvalue):
    if click_id=='':
        return
    token = kwIdToToken(pixelvalue)
    property=''
    senddata={
        "access_token":token,
        "clickid":click_id,
        "event_name":"EVENT_CONTENT_VIEW",
        "is_attributed":1,
        "mmpcode":"PL",
        "pixelId":pixelvalue,
        "pixelSdkVersion":"9.9.9",
        "properties":property,
        "testFlag":False,
        "third_party":"web",
        "trackFlag":False
    }
    url='http://www.adsnebula.com/log/common/api'
    header={
        "accept":"application/json;charset=utf-8",
        "Content-Type":"application/json"
    }
    s=requests.session()
    new_source=SourceAddressAdapter(settings.BIND_IP)
    s.mount('http://',new_source)
    s.mount('https://', new_source)
    response = s.post(url=url,headers=header,json=senddata)
    # response = requests.post(url=url,headers=header,json=senddata)
    #保存信息
    cinfo = models.uchannelinfo.objects(_id=uid).first()
    if not cinfo:
        models.uchannelinfo(_id=uid, click_id=click_id, fbc='', fbp='',adcode='Kwai for Business',pixelcode=pixelvalue).save()
    elif cinfo.click_id!=click_id or pixelvalue!=cinfo.pixelcode:
        models.uchannelinfo.objects(_id=uid).update(click_id=click_id,pixelcode=pixelvalue)

def viewSuccessCallBackFB(uid,fbc,fbp,pixelcode):
    if fbc=='' or fbp=='':
        return
    cinfo = models.uchannelinfo.objects(_id=uid).first()
    if not cinfo:
        models.uchannelinfo(_id=uid, click_id='', fbc=fbc, fbp=fbp, adcode='Unattributed',pixelcode=pixelcode).save()
    else:
        isUpdate = False
        if cinfo.fbc=='':
            isUpdate=True
            cinfo.fbc = fbc
        if cinfo.fbp=='':
            isUpdate=True
            cinfo.fbp = fbp
        if cinfo.pixelcode=='':
            isUpdate=True
            cinfo.pixelcode = pixelcode
        if isUpdate==True:
            models.uchannelinfo.objects(_id=uid).update(fbc=cinfo.fbc,fbp=cinfo.fbp,pixelcode=cinfo.pixelcode)

# 保存生成的订单
def saveNewPayOrder(_id,order_no,payType,shopId,shopType,price,click_id,uinfo,channelinfo):
    regFlag = 0
    subplatid = 0
    regFlag = uinfo.base.regFlag
    subplatid = uinfo.base.subplatid
    adcode = uinfo.base.adcode
    cinfo = models.uchannelinfo.objects(_id=uinfo._id).first()
    pixelcode = ''
    if not cinfo:
        models.uchannelinfo(_id=uinfo._id,click_id=click_id,fbc=channelinfo['fbc'],fbp=channelinfo['fbp'],HTTP_HOST=channelinfo['HTTP_HOST']).save()
    if click_id=='' and adcode=='Kwai for Business':
        if cinfo:
            click_id = cinfo.click_id
            pixelcode = cinfo.pixelcode
    u = models.orderinfo(_id=_id, fee=0, uid=uinfo._id, subTime=time.time(),
                         shopId=shopId, subPrice=price, backTime=0, backPrice=0, payType=payType,
                         order_no=order_no,
                         status=0, isChip=0, shopType=shopType, regFlag=regFlag, subplatid=subplatid,click_id=click_id,adcode=adcode,
                         ip = channelinfo['ip'],fbc=channelinfo['fbc'],fbp=channelinfo['fbp'],pixelcode=pixelcode,HTTP_HOST=channelinfo['HTTP_HOST'])
    u.save()
    if click_id!='':
        models.uchannelinfo.objects(_id=uinfo._id).update(click_id=click_id)
    if channelinfo['fbc']!='' and channelinfo['fbp']!='':
        models.uchannelinfo.objects(_id=uinfo._id).update(fbc=channelinfo['fbc'],fbp=channelinfo['fbp'])

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

def writeLog(str):
    logger = logging.getLogger('django')
    logger.info(str)

def qrcodeB64(qrcodedata):
    img = qrcode.make(qrcodedata)
    buf = io.BytesIO()
    img.save(buf)
    image_stream = buf.getvalue()
    heximage = base64.b64encode(image_stream).decode("utf-8")
    return heximage
# 订单成功通知定于频道
def chargeSuccessToPublish(uid,orderId):
    sendData={
        'c':'chargeBack',
        'uid':uid,
        'orderId':orderId
    }
    jsondata =  json.dumps(sendData)
    con = get_redis_connection()
    con.publish('all',jsondata)


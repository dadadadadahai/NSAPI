from . import models,Tools,paySuccess
import random,string
from django.conf import settings
from errorDefine import errorDefine
from django.http import HttpResponse
import hashlib,time,requests,logging,datetime,json
merchantId='128802'
secret='eRztKTREH1BBWri6Ytg5cAMJhZY5PAbk'
# merchantId='103'
# secret='17yfEzqOzr4f5QED3XgRj6jTZgs9yAJ5'
url='https://api.hkppay.com/api/open/merchant/trade/create'
def RequestPay(uid,shopId,price,uinfo,click_id,channelinfo):
    requestItem = {}
    requestItem['merchantId'] = merchantId
    requestItem['merchantOrderNo'] = models.CreateOrderUniqueId()
    requestItem['amount'] = price
    # requestItem['amount'] = 1
    requestItem['payType'] = 'PIX_QRCODE'
    requestItem['currency'] = 'BRL'
    requestItem['content'] ='score'
    requestItem['clientIp'] = channelinfo['ip']
    requestItem['callback'] = settings.CALLBACKHOST + 'hkpPayCallBack'
    requestItem0 = sorted(requestItem.keys())
    signstr = ''
    for keyval in requestItem0:
        if requestItem[keyval]=='':
            continue
        signstr = signstr + '&{}={}'.format(keyval, requestItem[keyval])
    signstr = signstr[1:]
    signstr = signstr + '&secret={}'.format(secret)
    m2 = hashlib.md5()
    m2.update(signstr.encode(encoding='utf-8'))
    sign = m2.hexdigest().lower()
    requestItem['sign'] = sign
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
    }
    r = requests.post(url,data=requestItem,headers=headers)
    jsonobj = r.json()
    print(jsonobj)
    jdata = jsonobj['data']
    if jsonobj['errorCode'] == 'SUCCESS':
        orderId = jdata['orderNo']
        qrCodeData = jdata['payRaw']
        Tools.saveNewPayOrder(requestItem['merchantOrderNo'], orderId, 'hkPay', shopId,
                             1, price, click_id, uinfo, channelinfo)
        rdata = {
            'errno': 0,
            'url': jdata['payUrl'],
            'orderNo': requestItem['merchantOrderNo'],
            'qrCodeData': qrCodeData,
            'img64': Tools.qrcodeB64(qrCodeData)
        }
        return rdata
    else:
        return {
            'errno': errorDefine.CHANNELERROR
        }

def hkpPayCallBack(request):
    if request.method == 'POST':
        jsonobj = request.POST
        requestItem0 = sorted(jsonobj.keys())
        signstr = ''
        for keyval in requestItem0:
            if keyval == 'sign' or jsonobj[keyval] == '':
                continue
            signstr = signstr + '&{}={}'.format(keyval, jsonobj[keyval])
        signstr = signstr[1:]
        signstr = signstr + '&secret={}'.format(secret)
        m2 = hashlib.md5()
        m2.update(signstr.encode(encoding='utf-8'))
        sign = m2.hexdigest().lower()
        if jsonobj['sign'] == sign and jsonobj['status'] == 'PAID':
            orderNo = jsonobj['merchantOrderNo']
            backprice = int(jsonobj['amount'])
            paySuccess.payBackSuccess(orderNo, backprice)
            return HttpResponse('success')
        else:
            return HttpResponse('FAIL')
        return HttpResponse('FAIL')

from . import models,Tools,paySuccess
import random,string
from django.conf import settings
from errorDefine import errorDefine
from django.http import HttpResponse
import hashlib,time,requests,logging,datetime,json
mchId='20001080'
md5Key='VLRCDGIJ0IOV6P49SACO8766RE7OSR1BAPEXF5YOK9VXUWUKMIDHQAYJXFZDBU8EZ6I75ALBTQJPVCCLHN0S6AMPGQUVMFITBUJS9YFVW4PSL7LTUFJNTOZKKWORAWAS'

def RequestPay(uid,shopId,price,uinfo,click_id,channelinfo):
    url='https://pay.goopago.com/api/unified/collection/create'
    requestItem = {}
    requestItem['mchId'] = mchId
    requestItem['nonceStr'] = generate_random_string(32)
    requestItem['mchOrderNo'] = models.CreateOrderUniqueId()
    requestItem['notifyUrl'] = settings.CALLBACKHOST + 'goopagooPayCallBack'
    requestItem['amount'] = price
    requestItem['payType'] = 140
    requestItem['email'] = 'name@example.com'
    requestItem['body']='test'
    requestItem0 = sorted(requestItem.keys())
    signstr = ''
    for keyval in requestItem0:
        if requestItem[keyval]=='':
            continue
        signstr = signstr + '&{}={}'.format(keyval, requestItem[keyval])
    signstr = signstr[1:]
    signstr = signstr + '&key={}'.format(md5Key)
    m2 = hashlib.md5()
    m2.update(signstr.encode(encoding='utf-8'))
    sign = m2.hexdigest().upper()
    requestItem['sign'] = sign
    jsonstr = json.dumps(requestItem)
    headers = {
        'Content-Type': 'application/json',
        'tmId':'br_auto'
    }
    r = requests.post(url, data=jsonstr, headers=headers)
    jsonobj = r.json()
    if jsonobj['resCode']=='SUCCESS':
        orderId = jsonobj['orderId']
        qrCodeData = jsonobj['reference']
        Tools.saveNewPayOrder(requestItem['mchOrderNo'], orderId, 'gooPagooPay', shopId,
                              1, price, click_id, uinfo, channelinfo)
        rdata = {
            'errno': 0,
            'url': jsonobj['url'],
            'orderNo': requestItem['mchOrderNo'],
            'qrCodeData': qrCodeData,
            'img64':Tools.qrcodeB64(qrCodeData)
        }
        return rdata
    else:
        return {
            'errno': errorDefine.CHANNELERROR
        }
def goopagooPayCallBack(request):
    if request.method == 'POST':
        postBody = request.body
        jsonobj = json.loads(postBody)
        requestItem0 = sorted(jsonobj.keys())
        signstr = ''
        for keyval in requestItem0:
            if keyval == 'sign' or jsonobj[keyval]=='':
                continue
            signstr = signstr + '&{}={}'.format(keyval, jsonobj[keyval])
        signstr = signstr[1:]
        signstr = signstr + '&key={}'.format(md5Key)
        m2 = hashlib.md5()
        m2.update(signstr.encode(encoding='utf-8'))
        sign = m2.hexdigest().upper()
        if jsonobj['sign'] == sign and jsonobj['status']==2:
            orderNo=jsonobj['mchOrderNo']
            backprice = int(jsonobj['amount'])
            paySuccess.payBackSuccess(orderNo,backprice)
            return HttpResponse('SUCCESS')
        else:
            return HttpResponse('FAIL')
        return HttpResponse('FAIL')
def generate_random_string(length):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for _ in range(length))
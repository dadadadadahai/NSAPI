from . import models
from . import Tools,paySuccess
from django.conf import settings
from errorDefine import errorDefine
from django.http import HttpResponse
import hashlib,time,requests,logging,datetime,json,qrcode
url = 'http://www.fast-pay.cc/gateway.aspx'
def RequestPay(uid,shopId,price,uinfo,click_id,channelinfo,paytype):
    FASTPAY = settings.FASTPAY
    requestItem = {}
    requestItem['mer_no'] = '1003878'
    requestItem['order_no'] = models.CreateOrderUniqueId()
    requestItem['order_amount'] = round(price/100)
    requestItem['payname'] = 'RM'
    requestItem['payemail'] = '2255848548@163.com'
    requestItem['payphone'] = '15689897451'
    requestItem['currency'] = 'MYR'
    requestItem['paytypecode'] = paytype
    requestItem['method'] = 'trade.create'
    requestItem['payshowtype'] = 1
    requestItem['returnurl'] = settings.CALLBACKHOST + 'FastPayCallBack'
    requestItem0 = sorted(requestItem.keys())
    signstr = ''
    for keyval in requestItem0:
        signstr = signstr + '&{}={}'.format(keyval, requestItem[keyval])
    signstr = signstr[1:]
    signstr = signstr + '{}'.format('4ef7778c3dc870084d1624630ff6dacc')
    m2 = hashlib.md5()
    m2.update(signstr.encode(encoding='utf-8'))
    sign = m2.hexdigest().lower()
    requestItem['sign'] = sign
    jsonstr = json.dumps(requestItem)
    headers = {
        'Content-Type': 'application/json'
    }
    logger = logging.getLogger('django')
    logger.info('jsonstr %s'%jsonstr)
    r = requests.post(url, data=jsonstr, headers=headers)
    jsonobj = r.json()
    if jsonobj['status'] == 'success':
        orderNo = requestItem['order_no']
        Tools.saveNewPayOrder(orderNo, jsonobj['order_no'], 'FastPay', shopId,
                              1, price, click_id, uinfo, channelinfo)
        qrCodeData = jsonobj['order_data']
        # 访问网页
        rdata = {
            'errno': 0,
            'url': jsonobj['order_link'],
            'orderNo': requestItem['order_no'],
            'qrCodeData': jsonobj['order_data'],
            'img64': Tools.qrcodeB64(qrCodeData)
        }
        return rdata
    else:
        logging.error('通道错误FastPay-{}'.format(r.json()))
        return {
            'errno': errorDefine.CHANNELERROR
        }

def FastPayCallBack(request):
    if request.method=='POST':
        FASTPAY = settings.FASTPAY
        postBody = request.body
        jsonobj = json.loads(postBody)
        key = '4ef7778c3dc870084d1624630ff6dacc'
        requestItem0 = sorted(jsonobj.keys())
        signstr = ''
        for keyval in requestItem0:
            if keyval=='sign':
                continue
            signstr = signstr + '&{}={}'.format(keyval, jsonobj[keyval])
        signstr = signstr[1:]
        signstr = signstr + '{}'.format(key)
        m2 = hashlib.md5()
        m2.update(signstr.encode(encoding='utf-8'))
        sign = m2.hexdigest().lower()
        if sign==jsonobj['sign'] and jsonobj['status']=='success':
            orderNo = jsonobj['order_no']
            backprice = float(jsonobj['order_amount']) * 100
            backprice = int(backprice)
            paySuccess.payBackSuccess(orderNo,backprice)
            return HttpResponse('ok')
        else:
            return HttpResponse('FAIL')
        return HttpResponse('FAIL')

def FastPayTestBack(request):
    postBody = request.body
    jsonobj = json.loads(postBody)
    orderNo = jsonobj['orderNo']
    backPrice=jsonobj['backPrice']
    paySuccess.payBackSuccess(orderNo, backPrice)
    return HttpResponse('ok')

from django.http import HttpResponse
from django.conf import settings
import hashlib,requests,logging,json
from . import models
import string,random
merchantId='128802'
secret='eRztKTREH1BBWri6Ytg5cAMJhZY5PAbk'
url='https://api.hkppay.com/api/open/merchant/payment/create'
def RepayRequest(repayOrder,phoneNum):
    accountType=''
    chavePix = repayOrder.chavePix
    if repayOrder.chavePixNum == 0:
        accountType='PIX_CPF'
    elif repayOrder.chavePixNum == 1:
        accountType='PIX_PHONE'
        chavePix = '+55' + chavePix
    elif repayOrder.chavePixNum==2:
        accountType='PIX_EMAIL'

    requestItem = {}
    requestItem['merchantId'] = merchantId
    requestItem['merchantOrderNo'] = repayOrder._id
    requestItem['amount'] = repayOrder.dinheiro
    requestItem['currency']='BRL'
    requestItem['accountType'] =accountType
    requestItem['accountNo'] = chavePix
    requestItem['accountName'] = repayOrder.name
    requestItem['callback'] = settings.REPAYCALLBACKHOST+'hkpPayCallBack'
    requestItem0 = sorted(requestItem.keys())
    signstr = ''
    for keyval in requestItem0:
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
    r = requests.post(url, data=requestItem, headers=headers)
    jsonobj = r.json()
    if not ('data' in jsonobj):
        #记录日志
        logger = logging.getLogger('django')
        logger.info('hkpRepay err{}'.format(r.json()))
    jdata = jsonobj['data']
    if jsonobj['errorCode'] == 'SUCCESS':
        repayOrder.state = 5
        repayOrder.orderId = jdata['orderNo']
        repayOrder.paytype = 'hkpPay'
        repayOrder.save()
    else:
        repayOrder.state = 4
        repayOrder.save()
        logger = logging.getLogger('django')
        logger.info('hkpRepay {}'.format(r.json()))

def hkpPayCallBack(request):
    if request.method == 'POST':
        data = request.POST
        postBody = request.body
        requestItem0 = sorted(data.keys())
        signstr = ''
        for keyval in requestItem0:
            if keyval == 'sign' or data[keyval] == '':
                continue
            signstr = signstr + '&{}={}'.format(keyval, data[keyval])
        signstr = signstr[1:]
        signstr = signstr + '&secret={}'.format(secret)
        m2 = hashlib.md5()
        m2.update(signstr.encode(encoding='utf-8'))
        sign = m2.hexdigest().lower()
        if sign == data['sign']:
            out_trade_no = data['merchantOrderNo']
            repayOrder = models.withdrawcash_order.objects(_id=out_trade_no).first()
            if repayOrder is None:
                return HttpResponse('FAIL')
            state = 3
            if data['status'] != 'PAID':
                state = 4
            repayOrder.state = state
            repayOrder.save()
            uid = repayOrder.uid
            if repayOrder.orderType == 2 and state == 3:
                extenrelation = models.extensionRelation.objects(_id=uid).first()
                if extenrelation:
                    extenrelation.tolCashOut = extenrelation.tolCashOut + repayOrder.dinheiro
                    extenrelation.save()
        return HttpResponse('success')
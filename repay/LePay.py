from django.http import HttpResponse
from django.conf import settings
import hashlib,requests,logging,json,datetime
from . import models
import json,urllib,userinfoCtr
from urllib import parse
url='https://payment.lexmpay.com/pay/transfer'
def RepayRequest(repayOrder,phoneNum):
    key = settings.LEPAY['repay_key']
    typeMap = ['CPF', 'PHONE', 'EMAIL']
    now = datetime.datetime.now()
    other_StyleTime = now.strftime("%Y-%m-%d %H:%M:%S")
    requestItem = {}
    requestItem['sign_type'] = 'MD5'
    requestItem['mch_id'] = settings.LEPAY['mch_id']
    requestItem['mch_transferId'] = repayOrder._id
    requestItem['transfer_amount'] = repayOrder.dinheiro/100
    requestItem['apply_date'] = other_StyleTime
    requestItem['bank_code'] = 'PIXPAY'
    requestItem['receive_name']='Pixpay'
    requestItem['receive_name'] =  repayOrder.name
    requestItem['receive_account'] = repayOrder.chavePix
    requestItem['document_type'] = typeMap[repayOrder.chavePixNum]
    requestItem['document_id'] = repayOrder.cpf
    requestItem['back_url']=settings.REPAYCALLBACKHOST+'LePayCallBack'
    requestItem0 = sorted(requestItem.keys())
    signstr = ''
    for keyval in requestItem0:
        if keyval=='sign_type':
            continue
        signstr = signstr+'&{}={}'.format(keyval,requestItem[keyval])
    signstr = signstr[1:]
    signstr = signstr + '&key={}'.format(key)
    m2 = hashlib.md5()
    m2.update(signstr.encode(encoding='utf-8'))
    sign = m2.hexdigest().lower()
    requestItem['sign'] = sign
    r = requests.post(url, data=requestItem)
    jsonobj =r.json()
    if jsonobj['tradeResult'] == '0':
        repayOrder.state = 5
        repayOrder.orderId = jsonobj['tradeNo']
        repayOrder.save()
    else:
        repayOrder.state = 4
        repayOrder.save()
        logging.error('体现接口LePay-{}'.format(r.json()))

def LePayCallBack(request):
    if request.method == 'POST':
        response = {}
        for postkey in request.POST:
            response[postkey] = parse.unquote(request.POST[postkey])
        key = settings.LEPAY['repay_key']
        requestItem0 = sorted(response.keys())
        signstr = ''
        for keyval in requestItem0:
            if keyval == 'signType' or keyval == 'sign':
                continue
            signstr = signstr + '&{}={}'.format(keyval, response[keyval])
        signstr = signstr[1:]
        signstr = signstr + '&key={}'.format(key)
        m2 = hashlib.md5()
        m2.update(signstr.encode(encoding='utf-8'))
        sign = m2.hexdigest().lower()
        if sign==response['sign']:
            out_trade_no = response['merTransferId']
            repayOrder = models.withdrawcash_order.objects(_id=out_trade_no).first()
            if repayOrder.state!=5:
                return HttpResponse('success')
            if int(response['tradeResult'])==1:
                repayOrder.state = 3
                repayOrder.save()
                uid = repayOrder.uid
                if repayOrder.orderType == 2:
                    extenrelation = models.extensionRelation.objects(_id=uid).first()
                    if extenrelation:
                        extenrelation.tolCashOut = extenrelation.tolCashOut + repayOrder.dinheiro
                        extenrelation.save()
            else:
                repayOrder.state = 4
                repayOrder.save()
    return HttpResponse('success')




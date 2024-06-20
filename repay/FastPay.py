from django.http import HttpResponse
from django.conf import settings
import hashlib,requests,logging,json
from . import models
url = 'http://www.fast-pay.cc/gateway.aspx'
FASTPAY = settings.FASTPAY
def RepayRequest(repayOrder,phoneNum):
    typeMap = ['CPF', 'PHONE', 'EMAIL']
    chavePix = repayOrder.chavePix
    if repayOrder.chavePixNum==1:
        chavePix = '+55'+chavePix
    key = '4ef7778c3dc870084d1624630ff6dacc'
    requestItem = {}
    requestItem['mer_no'] = '1003878'
    requestItem['order_no'] = repayOrder._id
    requestItem['method']='fund.apply'
    requestItem['order_amount'] = str(round(repayOrder.dinheiro/100,2))
    requestItem['currency'] = 'MYR'
    requestItem['acc_code'] = '123123'
    requestItem['acc_name'] = repayOrder.name
    requestItem['acc_no'] = chavePix
    requestItem['returnurl'] = settings.REPAYCALLBACKHOST+'FastPayCallBack'
    requestItem['province'] = repayOrder.cpf
    # requestItem['acc_phone'] = '55'+phoneNum
    requestItem['otherpara1'] =typeMap[repayOrder.chavePixNum]
    requestItem['otherpara2'] = 'RM'
    requestItem0 = sorted(requestItem.keys())
    signstr = ''
    for keyval in requestItem0:
        signstr = signstr+'&{}={}'.format(keyval,requestItem[keyval])
    signstr = signstr[1:]
    signstr = signstr + '{}'.format(key)
    m2 = hashlib.md5()
    m2.update(signstr.encode(encoding='utf-8'))
    sign = m2.hexdigest().lower()
    requestItem['sign'] = sign
    jsonstr = json.dumps(requestItem)
    headers = {
        'Content-Type': 'application/json'
    }
    r = requests.post(url, data=jsonstr, headers=headers)
    jsonobj = r.json()
    print(jsonobj)
    if jsonobj['status']=='success':
        repayOrder.state = 5
        repayOrder.orderId = jsonobj['sys_no']
        repayOrder.paytype = 'FastPay'
        repayOrder.save()
    else:
        repayOrder.state = 4
        repayOrder.save()
        logging.error('体现接口FastPay-{},{}'.format(r.json(),jsonstr))

def FastPayCallBack(request):
    if request.method == 'POST':
        postBody = request.body
        data = json.loads(postBody)
        requestItem = {}
        for key in data:
            requestItem[key] = data[key]
        requestItem0 = sorted(requestItem.keys())
        signstr = ''
        for keyval in requestItem0:
            if keyval == 'sign' or requestItem[keyval]=='':
                continue
            signstr = signstr + '&{}={}'.format(keyval, requestItem[keyval])
        signstr = signstr[1:]
        key = '4ef7778c3dc870084d1624630ff6dacc'
        signstr = signstr + '{}'.format(key)
        m2 = hashlib.md5()
        m2.update(signstr.encode(encoding='utf-8'))
        sign = m2.hexdigest().lower()
        if sign==requestItem['sign']:
            out_trade_no = data['order_no']
            repayOrder = models.withdrawcash_order.objects(_id=out_trade_no).first()
            if repayOrder is None:
                return HttpResponse('FAIL')
            state = 3
            if requestItem['result'] != 'success':
                state = 4
            repayOrder.state = state
            repayOrder.save()
            uid = repayOrder.uid
            if repayOrder.orderType == 2 and state==3:
                extenrelation = models.extensionRelation.objects(_id=uid).first()
                if extenrelation:
                    extenrelation.tolCashOut = extenrelation.tolCashOut + repayOrder.dinheiro
                    extenrelation.save()
        return HttpResponse('success')

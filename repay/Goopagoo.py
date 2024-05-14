from django.http import HttpResponse
from django.conf import settings
import hashlib,requests,logging,json
from . import models
import string,random
mchId='20001080'
md5Key='VLRCDGIJ0IOV6P49SACO8766RE7OSR1BAPEXF5YOK9VXUWUKMIDHQAYJXFZDBU8EZ6I75ALBTQJPVCCLHN0S6AMPGQUVMFITBUJS9YFVW4PSL7LTUFJNTOZKKWORAWAS'
def RepayRequest(repayOrder,phoneNum):
    url = 'https://pay.goopago.com/api/unified/agentpay/apply'
    accountType = 3
    chavePix = repayOrder.chavePix
    if repayOrder.chavePixNum==0:
        accountType = 1
    elif repayOrder.chavePixNum==1:
        chavePix = '+55' + chavePix
        accountType = 4
    requestItem = {}
    requestItem['mchId'] = mchId
    requestItem['nonceStr'] = generate_random_string(32)
    requestItem['mchOrderNo'] = repayOrder._id
    requestItem['notifyUrl'] = settings.REPAYCALLBACKHOST+'GoopagPayCallBack'
    requestItem['amount']  = repayOrder.dinheiro
    requestItem['accountName'] = repayOrder.name
    requestItem['accountNo'] = chavePix
    requestItem['idNumber'] = repayOrder.cpf
    requestItem['accountType'] =accountType
    requestItem0 = sorted(requestItem.keys())
    signstr = ''
    for keyval in requestItem0:
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
        repayOrder.state = 5
        repayOrder.orderId = jsonobj['orderId']
        repayOrder.paytype = 'GooPagoo'
        repayOrder.save()
    else:
        repayOrder.state = 4
        repayOrder.save()
        logger = logging.getLogger('django')
        logger.info('goopagRepay {}'.format(r.json()))

def GoopagPayCallBack(request):
    if request.method == 'POST':
        postBody = request.body
        data = json.loads(postBody)
        requestItem0 = sorted(data.keys())
        signstr = ''
        for keyval in requestItem0:
            if keyval == 'sign' or data[keyval] == '':
                continue
            signstr = signstr + '&{}={}'.format(keyval, data[keyval])
        signstr = signstr[1:]
        signstr = signstr + '&key={}'.format(md5Key)
        m2 = hashlib.md5()
        m2.update(signstr.encode(encoding='utf-8'))
        sign = m2.hexdigest().upper()
        if sign == data['sign']:
            out_trade_no = data['mchOrderNo']
            repayOrder = models.withdrawcash_order.objects(_id=out_trade_no).first()
            if repayOrder is None:
                return HttpResponse('FAIL')
            state = 3
            if data['status'] != 2:
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
def generate_random_string(length):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for _ in range(length))
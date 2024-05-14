#体现体现
url = 'https://tspay.online/appclient/withdraw.do'
from django.http import HttpResponse
from django.conf import settings
import hashlib,requests,logging,json
from . import models
#体现申请
def RepayRequest(repayOrder,phoneNum):
    typeMap=['CPF','PHONE','EMAIL']
    email = '123123@163.com'
    if repayOrder.chavePixNum==2:
        email = repayOrder.chavePix
    elif repayOrder.chavePixNum==1:
        repayOrder.chavePix = '55'+repayOrder.chavePix
    requestItem = {}
    requestItem['appid'] = settings.TSPAY['AppId']
    requestItem['out_trade_no'] = repayOrder._id
    requestItem['type'] = 4
    requestItem['name'] = repayOrder.name
    requestItem['mobile'] = '55'+phoneNum
    requestItem['amount'] = repayOrder.dinheiro
    requestItem['currency'] ='BRL'
    requestItem['version']='v1.0'
    requestItem['notify_url'] = settings.REPAYCALLBACKHOST+'TsPayCallBack'
    requestItem['document_id'] = repayOrder.cpf
    requestItem['pix_type'] =typeMap[repayOrder.chavePixNum]
    requestItem['pix_key'] = repayOrder.chavePix
    requestItem0 = sorted(requestItem.keys())
    signstr = ''
    for keyval in requestItem0:
        signstr = signstr+'&{}={}'.format(keyval,requestItem[keyval])
    signstr = signstr[1:]
    key = settings.TSPAY['Key']
    signstr = signstr + '&key={}'.format(key)
    m2 = hashlib.md5()
    m2.update(signstr.encode(encoding='utf-8'))
    sign = m2.hexdigest().upper()
    requestItem['sign'] = sign
    # print(requestItem)
    r = requests.post(url, data=requestItem)
    jsonobj = r.json()
    if jsonobj['code']==0:
        data=jsonobj['data']
        repayOrder.state = 5
        repayOrder.orderId = data['order_no']
        repayOrder.save()
    else:
        repayOrder.state = 4
        repayOrder.save()
        logging.error('体现接口TsPay-{}'.format(r.json()))

def TsPayCallBack(request):
    if request.method == 'POST':
        postBody = request.body
        jsonobj = json.loads(postBody)
        data = jsonobj['data']
        requestItem = {}
        for key in data:
            requestItem[key] = data[key]
        requestItem0 = sorted(requestItem.keys())
        signstr = ''
        for keyval in requestItem0:
            if keyval=='sign':
                continue
            signstr = signstr + '&{}={}'.format(keyval, requestItem[keyval])
        signstr = signstr[1:]
        key = settings.TSPAY['Key']
        signstr = signstr + '&key={}'.format(key)
        m2 = hashlib.md5()
        m2.update(signstr.encode(encoding='utf-8'))
        sign = m2.hexdigest().upper()
        if sign==requestItem['sign']:
            out_trade_no = data['out_trade_no']
            repayOrders = models.withdrawcash_order.objects(_id=out_trade_no)
            if len(repayOrders) <= 0:
                return
            repayOrder = repayOrders[0]
            state = 3
            if jsonobj['code']==-1:
                state = 4
            repayOrder.state=state
            repayOrder.save()
            uid = repayOrder.uid
            if repayOrder.orderType==2:
                extenrelation = models.extensionRelation.objects(_id=uid).first()
                if extenrelation:
                    extenrelation.tolCashOut =extenrelation.tolCashOut + repayOrder.dinheiro
                    extenrelation.save()
    return HttpResponse('SUCCESS')
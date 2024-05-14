from django.http import HttpResponse
from django.conf import settings
import hashlib,requests,logging,json,datetime
from . import models
import json,urllib
from urllib import parse
import json,base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
url = 'https://realpay.ltd/df/gateway/proxyrequest'
def RepayRequest(repayOrder,phoneNum):
    requestItem = {}
    requestItem['head']={
        'mchtId':settings.INAY['mchtId'],
        'version':'20',
        'biz':'df104',
    }
    cerType = '1'
    if repayOrder.chavePixNum==0:
        cerType = '0'
    elif repayOrder.chavePixNum==1:
        cerType = '2'
    elif repayOrder.chavePixNum==2:
        cerType = '3'
    body={
        'batchOrderNo':repayOrder._id,
        'totalNum':1,
        'totalAmount':repayOrder.dinheiro,
        'notifyUrl':settings.REPAYCALLBACKHOST+'InterFaceCallBack',
        'currencyType':'BRL',
        'detail':[{
            'seq':'1',
            'amount':repayOrder.dinheiro,
            'accType':'0',
            'certType':cerType,
            'certId':str(repayOrder.chavePix).strip(),
            'bankCardNo':str(repayOrder.cpf).strip(),
            'bankCardName':str(repayOrder.name).strip(),
        }],
    }
    #  对body 进行rsa加密
    requestItem['body'] = urllib.parse.quote(rsa_encrypt(json.dumps(body,ensure_ascii=False)))
    r = requests.post(url, json=requestItem)
    jsonobj = r.json()
    if jsonobj['head']['respCode']=='0000':
        bodyjson = json.loads(rsa_decrypt(urllib.parse.unquote(jsonobj['body'])))
        repayOrder.state = 5
        repayOrder.orderId = bodyjson['tradeId']
        repayOrder.save()
    else:
        repayOrder.state = 4
        repayOrder.save()
        logging.error('体现接口InterFace-{}'.format(r.json()))

def InterFaceCallBack(request):
    if request.method == 'POST':
        postBody = request.body
        jsonobj = json.loads(postBody)
        if jsonobj['head']['respCode']=='0000':
            bodyjson = rsa_decrypt(urllib.parse.unquote(jsonobj['body']))
            if bodyjson:
                bodyobj = json.loads(bodyjson)
                out_trade_no = bodyobj['batchOrderNo']
                repayOrder = models.withdrawcash_order.objects(_id=out_trade_no).first()
                for i in bodyobj['detail']:
                    if i['status']=='SUCCESS':
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
                    break
    return HttpResponse('SUCCESS')

def rsa_encrypt(msg,max_length=100):
    cipher_rsa = PKCS1_v1_5.new(RSA.import_key(settings.INAY['public']))
    res_byte = bytes()
    for i in range(0, len(msg), max_length):
        res_byte += cipher_rsa.encrypt(msg[i:i + max_length].encode('utf-8'))
    return base64.b64encode(res_byte).decode('utf-8')
def rsa_decrypt(msg, max_length=128):
    """
    RSA解密
    :param msg: 加密字符串
    :param pri_path: 私钥路径
    :param max_length: 1024bit的秘钥用128，2048bit的秘钥用256位
    :return:
    """
    key = RSA.import_key(settings.INAY['private'])
    cipher = PKCS1_v1_5.new(key)
    res_bytes = bytes()
    # missing_padding = 4 - len(msg) % 4
    # if missing_padding:
    #     msg += '=' * missing_padding
    encrypt_data = base64.b64decode(msg)
    for i in range(0, len(encrypt_data), max_length):
        res_bytes += cipher.decrypt(encrypt_data[i:i + max_length],0)
    return res_bytes.decode('utf-8')
from django.http import HttpResponse
from django.conf import settings
import hashlib,requests,logging,json
from . import models
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
import base64
privateKey='''-----BEGIN PRIVATE KEY-----
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
-----END PRIVATE KEY-----'''
#平台公钥
publishKey='''-----BEGIN PUBLIC KEY-----
MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEA2esz0qQ2WuF99mYYvgLFUs1J7m8bQAvwfi7fJud7WChUpGH3zrITfsvMzlBoixUuxFm7fInCYqwJuSAndOHIkQgeSuLsOsMk7vbFsHF2+KvJzQB2YcywmUVqn9mCztDjuIIC2aDFHUgiSjAF6jb6MxAzhDze3wwEfcQyxvoLVcDPazCH/ID2VzHTMKkluzvg6Oupxju/Y5mJSbRH8XT4fILkCY9ZIcveYC7fftuQfRsGHXFwj6Punfxryk0pLMbiItDl+rKZ3Dxj5xoR5gi4WkQ2qPSWxVRpQhrMP3EIkxH/qb2ZouBpIPId3HNwK27lLvW99DzlyInW5Iab5zgq6Ref8qXANPH36Fdpbx9fEFZEKzzER0i85iqGzn0IzOHMzK8lpHmX/2XgKF5MVZj67fj/XbCWEyfMENnopc6IaM7e0BLGziaJ6xUz1gugRBwg+qq8PAuYuOKV7ZrkIIiu2Qd0d2gd1F8tEFdQFgPHcoxBnPt/i4EOOmoM7lIodGcP/NshRFZMI1gMNuH22DZmH7ZkdBAyTT7bY4uZNpC/38YpT+bW6QfheXdRt4Mas8hPXP8CZ5HT/HjmaQ6CeO++wpFSDovmY/W/5le0rybMxuy/OS9ILUS09bjKzeDVSGYC42AyunZc3H228uinZDvmdJkABY+i/3RyCDOorPLradkCAwEAAQ==
-----END PUBLIC KEY-----'''

xAccount='1200cd24-cf5c-410f-b733-0acb75c6c78c'
def RepayRequest(repayOrder,phoneNum):
    url = "https://v2.payout.sitobank.com/pixkey"
    repayType = 1
    if repayOrder.chavePixNum==0:
        repayType=1
    elif repayOrder.chavePixNum==1:
        repayType=4
    elif repayOrder.chavePixNum==2:
        repayType=3
    chavePix = repayOrder.chavePix
    if repayOrder.chavePixNum==1:
        chavePix = '+55'+chavePix
    payload = json.dumps({
        "mchOrderNo": str(repayOrder._id),
        "notifyUrl": settings.REPAYCALLBACKHOST+'SitoBankCallBack',
        "amount": repayOrder.dinheiro,
        'idNumber':repayOrder.cpf,
        "accountName": repayOrder.name,
        "accountNo": chavePix,
        "accountType": repayType,
    })
    headers = {
        'X-Account': xAccount,
        'X-Signature': encodeRSA(payload,privateKey) ,
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    jsonobj =  response.json()
    print(jsonobj)
    if jsonobj['status']==11:
        repayOrder.state = 5
        repayOrder.orderId = jsonobj['orderNo']
        repayOrder.paytype = 'SitoBank'
        repayOrder.save()
    else:
        repayOrder.state = 4
        repayOrder.save()
        logging.error('体现接口SitoBank-{}'.format(response.json()))

def SitoBankCallBack(request):
    xAccount = request.headers['X-Account']
    xSignature = request.headers['X-Signature']
    postBody = request.body
    print(postBody)
    try:
        decodeRSA(postBody.decode(), xSignature, publishKey)
        # 签名验证通过
        jsonobj = json.loads(postBody)
        orderNo = jsonobj['mchOrderNo']
        backprice = jsonobj['amount']
        repayOrder = models.withdrawcash_order.objects(_id=orderNo).first()
        if repayOrder is None:
            return HttpResponse('FAIL')
        state = 3
        if jsonobj['status'] ==4:
            state = 4
        repayOrder.state = state
        repayOrder.save()
        uid = repayOrder.uid
        if repayOrder.orderType == 2 and state == 3:
            extenrelation = models.extensionRelation.objects(_id=uid).first()
            if extenrelation:
                extenrelation.tolCashOut = extenrelation.tolCashOut + repayOrder.dinheiro
                extenrelation.save()
    except Exception as e:
        print(e)
    return HttpResponse('ok')


def encodeRSA(message: str, privKey: str) -> str:
    pkey = RSA.importKey(privKey)

    h = SHA256.new(message.encode())
    signature = pkcs1_15.new(pkey).sign(h)
    return base64.b64encode(signature).decode()

def decodeRSA(message: str, sign: str, pubKey: str) -> str:
    pkey = RSA.importKey(pubKey)

    h = SHA256.new(message.encode())
    return pkcs1_15.new(pkey).verify(h, base64.b64decode(sign))
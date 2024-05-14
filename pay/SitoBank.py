from . import models
from . import Tools,paySuccess
from django.conf import settings
from errorDefine import errorDefine
from django.http import HttpResponse
import hashlib,time,requests,logging,datetime,json,qrcode
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
import base64



# privateKey ='''-----BEGIN PRIVATE KEY-----
# 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
# -----END PRIVATE KEY-----'''
#
# privateKey='''-----BEGIN PRIVATE KEY-----
# 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
# -----END PRIVATE KEY-----'''
# #平台公钥
# publishKey='''-----BEGIN PUBLIC KEY-----
# MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEA2esz0qQ2WuF99mYYvgLFUs1J7m8bQAvwfi7fJud7WChUpGH3zrITfsvMzlBoixUuxFm7fInCYqwJuSAndOHIkQgeSuLsOsMk7vbFsHF2+KvJzQB2YcywmUVqn9mCztDjuIIC2aDFHUgiSjAF6jb6MxAzhDze3wwEfcQyxvoLVcDPazCH/ID2VzHTMKkluzvg6Oupxju/Y5mJSbRH8XT4fILkCY9ZIcveYC7fftuQfRsGHXFwj6Punfxryk0pLMbiItDl+rKZ3Dxj5xoR5gi4WkQ2qPSWxVRpQhrMP3EIkxH/qb2ZouBpIPId3HNwK27lLvW99DzlyInW5Iab5zgq6Ref8qXANPH36Fdpbx9fEFZEKzzER0i85iqGzn0IzOHMzK8lpHmX/2XgKF5MVZj67fj/XbCWEyfMENnopc6IaM7e0BLGziaJ6xUz1gugRBwg+qq8PAuYuOKV7ZrkIIiu2Qd0d2gd1F8tEFdQFgPHcoxBnPt/i4EOOmoM7lIodGcP/NshRFZMI1gMNuH22DZmH7ZkdBAyTT7bY4uZNpC/38YpT+bW6QfheXdRt4Mas8hPXP8CZ5HT/HjmaQ6CeO++wpFSDovmY/W/5le0rybMxuy/OS9ILUS09bjKzeDVSGYC42AyunZc3H228uinZDvmdJkABY+i/3RyCDOorPLradkCAwEAAQ==
# -----END PUBLIC KEY-----'''
#
# xAccount='1200cd24-cf5c-410f-b733-0acb75c6c78c'
privateKey='''-----BEGIN PRIVATE KEY-----
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
-----END PRIVATE KEY-----'''

publishKey='''-----BEGIN PUBLIC KEY-----
MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAvBq7PL4SHjPq0xclitLVc5hX+kHfzqqM+3rED3ENA3Ck4yHpbzcjsEMPyLXMHYNSW9OVH9QLgdB/A32hQg8GW8EMMfyFe2HLDgBE52XoWDg32QakQ259BWwKQhBCag4Td3kHVqaUUfC5FDXEUVwLYKyGjAQzpfxwrah2OZfBadG1Pz9MkAkPq7rtAdBuuujQQubiszTjYEN5ph3uaS4WEv+rwFlDJdsufNLzL6dD+tVtGJ88GsYlQVPP2I3k0OxhVLMkPR70kkuHZMkFMmdrHWt+Vmq7O+29MSwiIn5bTheMVA4kDCi4/177wLdD5DXvAAR0GEXNmDovoWnQSeEiKsG+Br6t8hxdWOGSXJYsPyxGvutpICcnHsJHh0TTPoBYiUvWJhTqRdmbiEuhXKt69jFxnPIVv908ui01XYpVu+pcL519VgjvTym1/vmK1ey3kk08UCnzQBp4HPezRvgPqe8Z4sfnM7U8W41pycpOiYJwURr83VkcOthuLrgcuRfYzxJFcMLf1JZUAdF5TNLJp5n2GUU1a1nIQi8bkoP7G9pRUscVXTbf/pSq6LwCms6cDw+uRdE2xVUNy1vyVOHAZTjyBBrQf/vejbDIXTshSYU6AJcqL2xlrAxaybDva/LXPgcQmiUFyYprqAg9l5Sr50FYJJ1wUJh4HJct7pjB+NECAwEAAQ==
-----END PUBLIC KEY-----'''

xAccount='b5373276-3924-4fbb-8845-acd15e910543'

def RequestPay(uid,shopId,price,uinfo,click_id,channelinfo):
    url = "https://v2.invoice.sitobank.com/create"
    mchOrderNo = models.CreateOrderUniqueId()
    payload = json.dumps({
        "mchOrderNo":  mchOrderNo,
        "amount": price,
        "name": "jack",
        "subject": "buychip",
        "body": "one laptap",
        "notifyUrl": settings.CALLBACKHOST + 'SitoBankCallBack',
    })
    headers = {
        # 'X-Account': '1200cd24-cf5c-410f-b733-0acb75c6c78c',
        'X-Account':xAccount,
        'X-Signature': encodeRSA(payload,privateKey) ,
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
        'Content-Type': 'application/json'
    }
    print('data',payload)
    print('head',headers)
    response = requests.request("POST", url, headers=headers, data=payload)
    jsonobj =  response.json()
    print(jsonobj)
    if jsonobj['status']==2:
        orderNo=mchOrderNo
        Tools.saveNewPayOrder(orderNo, jsonobj['orderNo'], 'SitoBank', shopId,
                              1, price, click_id, uinfo, channelinfo)
        qrCodeData=jsonobj['reference']
        rdata = {
            'errno': 0,
            'url': jsonobj['url'],
            'orderNo': orderNo,
            'qrCodeData': qrCodeData,
            'img64': Tools.qrcodeB64(qrCodeData)
        }
        return rdata
    else:
        logging.error('通道错误SitoBank-{}'.format(response.json()))
        return {
            'errno': errorDefine.CHANNELERROR
        }
def SitoBankCallBack(request):
    #检查http头
    xAccount= request.headers['X-Account']
    xSignature =request.headers['X-Signature']
    postBody = request.body
    try:
        decodeRSA(postBody.decode(),xSignature,publishKey)
        #签名验证通过
        jsonobj = json.loads(postBody)
        if jsonobj['status']==3:
            print('status 3')
            orderNo = jsonobj['mchOrderNo']
            backprice = jsonobj['payments']['orderAmount']
            paySuccess.payBackSuccess(orderNo, backprice)
            return HttpResponse('ok')
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
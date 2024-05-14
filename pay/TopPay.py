from . import models,Tools,paySuccess
import random,string
from django.conf import settings
from errorDefine import errorDefine
from django.http import HttpResponse
import hashlib,time,requests,logging,datetime,json

import rsa

url='https://bra-openapi.toppay.asia/gateway/prepaidOrder'

privateKey='''-----BEGIN PRIVATE KEY-----
MIICdwIBADANBgkqhkiG9w0BAQEFAASCAmEwggJdAgEAAoGBAL5Bbm+YEJ5oxJ1Hr1wIOYSR+ZXn7u3WUKWl70Oj5tqE+Ks1Z9FpcWlUdRdJY4UxfZPU0t4ceMp9tmpKz9cb+K3Gi6vpes7S5f/G2f1aatkVIRaxA80YOOtfWnxxZ+02c8sEYanyIpMfFMgnXhHeA9OjXvtEaMXj/8AIUl+zEA6XAgMBAAECgYAt2PS0/a8bjWG8CRdQFUdPFCJSJpckR14d3PPgl/G8vQhzsaX4B/HlkQ26c9wAr+F0K3g5QCE3or2/tZGKY9o0E1hXx/4K8BVbfaffem4M6KFxn6fgBZNoBhAlMsSm2X8RVMUf6fnOhTj7OyvfLC6efivkwXSP8GxEpvQoE8HcgQJBAPQu7LzGJ93mNapoGvTDVrR3TNctsu14htrR78e2s7GALzGbeNtSRrxWnayf9Ndb776raIJ3wnAMXz/xCF26o1cCQQDHdmvBBwPN4V7qg1cNsR28lTKxmIKyNYv27C+zmU4rCaP2lxuPnOv4SRePbK+5GIEdYWxyyMZLPqedlvZeRCbBAkBgH8TT/1GcWc6QeZD6/5a3TitynavNLeAwbeptfS+51VM+vQxTkk0EQTiqxwE0ch2ruoBWs9xYDZbFbhY0B4/bAkEAsQgq9SS7vKRV8QDnZ/CWewVU/AlnnrIl6t+QKvBbT5l73GYbgSh+y1xcO+D0Se0005XfgjUuwiP28sjFG7+TQQJBANH4vmuU13jknTTUFq6DIUz7a2GIRtOWI87t3/Xq+jrVbaliDAHezKaOWoLeLOfoKiqmtC6IRfLibsGVZMFo/o4=
-----END PRIVATE KEY-----'''
# 平台公钥
publishKey='''-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCKS+uhobMcZGy8Quwa2h0E389vm4Ew/oIJELBsviuaJn6PXRaYvVCtZ6CYa1rHoSaPAjS32B76mDMz7ZI7XrEJMTTr8boTdP4oicTj2fL6h1l31r5Ai6fWj6Ghfm3PEkgUappZSM7eP9dm1l4hj3tkC7wL7MdXckOttIOy4DgB/wIDAQAB
-----END PUBLIC KEY-----'''
merchantCode = 'S820240410122234000001'

def RequestPay(uid,shopId,price,uinfo,click_id,channelinfo):
    requestItem = {}
    requestItem['merchantCode'] =merchantCode
    requestItem['orderType'] = '0'
    requestItem['orderNum'] = models.CreateOrderUniqueId()
    requestItem['payMoney'] = round(price,2)
    requestItem['notifyUrl'] = settings.CALLBACKHOST + 'TopPayCallBack'
    requestItem['sign'] = ''
    requestItem0 = sorted(requestItem.keys())
    signstr = ''
    for keyval in requestItem0:
        if requestItem[keyval] == '':
            continue
        signstr = signstr + '{}'.format(requestItem[keyval])



def encrypt(msg):
    rsastr=rsa.encrypt(msg,privateKey)
    
from django.http import JsonResponse
from django.conf import settings
from . import models,Tools
import time
def payTest(uid,shopId,price):
    requestItem = {}
    requestItem['out_trade_no'] = models.CreateOrderUniqueId()
    requestItem['type'] = 1
    requestItem['amount'] = price
    requestItem['currency'] = 'BRL'
    requestItem['callback_url'] = 'http://127.0.0.1'
    requestItem['notify_url'] = settings.CALLBACKHOST + 'TsPayCallBack'
    requestItem['version'] = 'v1.0'
    #记录成功订单
    models.orderinfo(_id=requestItem['out_trade_no'], fee=0, uid=uid, subTime=time.time(), shopId=shopId,
                         subPrice=price, backTime=time.time(), backPrice=price, payType='TsPay', order_no="123456", status=1,
                         isChip=0).save()
    models.rebateFinal(uid=uid, price=price, addTime=time.time(), orderNo=requestItem['out_trade_no']).save()
    Tools.chargeSuccessToPublish(uid,requestItem['out_trade_no'])
    qrCodeData='https://www.baidu.com'
    rdata = {
        'errno': 0,
        'url': "https://www.test.com",
        'orderNo': requestItem['out_trade_no'],
        'qrCodeData': qrCodeData,
        'img64': Tools.qrcodeB64(qrCodeData)
    }
    return rdata
#支付成功后处理
from . import models,Tools
import time
def payBackSuccess(orderNo,backprice):
    orderinfo = models.orderinfo.objects(_id=orderNo).first()
    if orderinfo and orderinfo.status == 0:
        orderinfo.backPrice = backprice
        orderinfo.backTime = time.time()
        orderinfo.status = 1
        orderinfo.save()
        # 处理返利通知
        models.rebateFinal(uid=orderinfo.uid, price=orderinfo.backPrice, addTime=time.time(),
                           orderNo=orderinfo._id).save()
        # redis 反推
        Tools.chargeSuccessToPublish(orderinfo.uid, orderNo)
        adcode = orderinfo.adcode
        click_id = orderinfo.click_id
        ip = orderinfo.ip
        fbc = orderinfo.fbc
        fbp = orderinfo.fbp
        uid = orderinfo.uid
        pixelcode = orderinfo.pixelcode
        HTTP_HOST = orderinfo.HTTP_HOST
        ucinfo = models.uchannelinfo.objects(_id=uid).first()
        if ucinfo:
            if fbc == '':
                fbc = ucinfo.fbc
            if fbp == '':
                fbp = ucinfo.fbp
            if pixelcode == '':
                pixelcode = ucinfo.pixelcode
            if HTTP_HOST == '':
                HTTP_HOST = ucinfo.HTTP_HOST
            if click_id=='':
                click_id = ucinfo.click_id
        # 上报快手
        if adcode == 'Kwai for Business':
            Tools.paySuccessCallBackKW(orderinfo.backPrice, click_id, orderinfo.shopId, pixelcode)
            # 上报facebook
        elif adcode == 'Unattributed':
            Tools.paySuccessCallBackFirst(orderinfo.uid, orderinfo.backPrice, ip, fbc, fbp, pixelcode,HTTP_HOST, ucinfo)
            Tools.paySuccessCallBackFb(orderinfo.backPrice, ip, fbc, fbp, pixelcode, HTTP_HOST)
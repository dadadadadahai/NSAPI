import time,math

from django.http import JsonResponse
from . import models,TsPay,TestRePay,LePay,InterFacePay,FastPay,Goopagoo,hkpPay,SitoBank
from errorDefine import errorDefine
from datetime import datetime
import userinfoCtr
# Create your views here.
#提现流水
def repayState(request,orderNo,channelNo):
    repayOrders  = models.withdrawcash_order.objects(_id=orderNo)
    if len(repayOrders)<=0:
        return  JsonResponse({'errno':errorDefine.NoRepayOrder})
    repayOrder = repayOrders[0]
    phoneNum = ''
    if repayOrder.state==4 or repayOrder.state==6:
        return JsonResponse({'errno':1})
    if repayOrder.chavePixNum==1:
        phoneNum = repayOrder.chavePix
    else:
        uinfos = models.userinfo.objects(_id=repayOrder.uid)
        uinfo = uinfos[0]
        phoneNum = uinfo.base.phoneNbr
    if channelNo==1:  #tspay 体现
        FastPay.RepayRequest(repayOrder,phoneNum)
    elif channelNo==2:
        FastPay.RepayRequest(repayOrder,phoneNum)
    elif channelNo==3:
        FastPay.RepayRequest(repayOrder,phoneNum)
    elif channelNo==4:
        FastPay.RepayRequest(repayOrder,phoneNum)
    elif channelNo==5:
        FastPay.RepayRequest(repayOrder,phoneNum)
    elif channelNo == 6:
        hkpPay.RepayRequest(repayOrder, phoneNum)
    return JsonResponse({'errno':0})
#添加返利订单
def repayRelationAddOrder(request,uid):
    uinfo =models.extensionRelation.objects(_id=uid).first()
    if uinfo is None:
        return JsonResponse({'errno':errorDefine.NOUSER})
    if uinfo.rebatechip<100:
        return JsonResponse({'errno':errorDefine.MoneyNotEnough})
    #添加体现订单
    rebatechip = math.floor(uinfo.rebatechip)
    #增加订单
    if addRepayOrder(uid,rebatechip):
        models.extensionRelation.objects(_id=uid).update(rebatechip = uinfo.rebatechip - rebatechip)
        return JsonResponse({'errno':0})
    else:
        return JsonResponse({'errno':errorDefine.Other})

def addRepayOrder(uid,rebatechip):
    #查询基础信息
    basedrawcash = models.withdrawcash.objects(_id=uid).first()
    if basedrawcash is None:
        return False
    if basedrawcash.cpf is None or basedrawcash.name is None or basedrawcash.chavePix is None:
        return False
    id = models.CreateOrderUniqueId()
    models.withdrawcash_order(_id=id,uid=uid,name=basedrawcash.name,timestamp=time.time(),
                              chavePix=basedrawcash.chavePix,cpf=basedrawcash.cpf,
                              chavePixNum = basedrawcash.flag,moedas=rebatechip,dinheiro=rebatechip,
                              times=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),orderType=2).save()
    return True
def repayRebatQuery(request,uid,page):
    skipnum = (page - 1) * 50
    orders = models.withdrawcash_order.objects(uid=uid,orderType=2).skip(skipnum).limit(50).order_by('-_id')
    rdata = []
    for order in orders:
        rdata.append({'_id':order._id,'chavePixNum':order.chavePixNum,
                      'moedas':order.moedas,'dinheiro':order.dinheiro,
                      'times':order.times,'state':order.state})
    return JsonResponse({'errno':errorDefine.SUCCESS,
                         'datas':rdata})
from django.http import JsonResponse
from . import models
from errorDefine import errorDefine
import time,datetime
#查询本人数据概要
def queryNumVal(request,uid):
    uinfo = models.userinfo.objects(_id=uid).first()
    if not uinfo:
        return JsonResponse({"errno":errorDefine.NOUSER})
    #查询推广关系统计表
    exteninfo = models.extensionRelation.objects(_id=uid).first()
    if not exteninfo:
         exteninfo=models.extensionRelation(_id=uid,parents=[])
         exteninfo.save()
    #取当日时间戳
    todaycls =  datetime.datetime.today()
    year,month,day =  todaycls.year,todaycls.month,todaycls.day
    #取记录时间戳
    if exteninfo.addFlowingTimes>0:
        stampTimes =  datetime.datetime.fromtimestamp(exteninfo.addFlowingTimes)
        if year!=stampTimes.year or month!=stampTimes.month or day!=stampTimes.day:
            exteninfo.todayFlowingChips += exteninfo.tomorrowFlowingChips
            exteninfo.tomorrowFlowingChips = 0
            exteninfo.addFlowingTimes = time.time()
            exteninfo.save()
    validinViteNum = 0
    validinViteFreeNum = 0
    validinViteChips = 0
    tmpvaild =  models.validinvite.objects(_id=uid).first()
    if tmpvaild:
        validinViteNum = len(tmpvaild.validinViteList)
        validinViteFreeNum = len(tmpvaild.validinViteFreeList)
        validinViteChips = tmpvaild.validinViteChips
    #构建返回数据
    return JsonResponse({
        "errno":errorDefine.SUCCESS,
        "rebatechip":exteninfo.rebatechip,
        "belowNum":exteninfo.belowNum,
        "tolBelowCharge":exteninfo.tolBelowCharge,
        "tolrebate":exteninfo.tolrebate,
        'tomorrowFlowingChips':exteninfo.tomorrowFlowingChips,
        'todayFlowingChips':exteninfo.todayFlowingChips,
        'tolBetAll':exteninfo.tolBetAll,
        'tolBetFall':exteninfo.tolBetFall,
        'freeValidinViteChips':exteninfo.freeValidinViteChips,
        "lowrebatechip":500,        #提现最低金额
        "validinViteNum":validinViteNum,
        'validinViteFreeNum':validinViteFreeNum,
        'validinViteChips':  validinViteChips,
    })
def queryvalidinvitelogDay(request,uid,page):
    day_time = int(time.mktime(datetime.date.today().timetuple()))
    skipnum = (page - 1) * 20
    dinfos = models.validinvitelog.objects(uid=uid, type=1,addTime__gte=day_time,validinViteNum__gt=0).skip(skipnum).limit(20).order_by('-addTime')
    rdata = []
    for dval in dinfos:
        validinViteNum=dval.validinViteNum
        childId=dval.childId
        if validinViteNum is None:
            validinViteNum = 0
        if childId is None:
            childId=0
        rdata.append(
            {'uid': dval.uid, 'addChips': dval.addChips, 'validinViteNum': validinViteNum, 'addTime': dval.addTime,
             'childId':childId })
    return JsonResponse({"errno": errorDefine.SUCCESS, 'datas': rdata})
def queryvalidinvitelog(request,uid,page):
    skipnum = (page - 1) * 20
    dinfos = models.validinvitelog.objects(uid=uid,type=1,validinViteNum__gt=0).skip(skipnum).limit(20).order_by('-addTime')
    rdata = []
    for dval in dinfos:
        validinViteNum = dval.validinViteNum
        childId = dval.childId
        if validinViteNum is None:
            validinViteNum = 0
        if childId is None:
            childId = 0
        rdata.append(
            {'uid': dval.uid, 'addChips': dval.addChips, 'validinViteNum': validinViteNum, 'addTime': dval.addTime,
             'childId': childId})
    return JsonResponse({"errno": errorDefine.SUCCESS, 'datas': rdata})

#查询给自己返利最多的下线id信息
def queryMaxRebateBelow(request,uid,page):
    skipnum = (page-1)*50
    dinfos = models.rebateItem.objects(uid=uid).skip(skipnum).limit(50).order_by('-chip')
    rdata=[]
    for dval in dinfos:
        rdata.append({'childId':dval.childId,'chip':dval.chip,'tchip':dval.tchip,'betchip':dval.betchip,'tbetchip':dval.tbetchip,'lev':dval.lev})
    return JsonResponse({"errno":errorDefine.SUCCESS,'datas':rdata})
#查询返利日志
def queryLog(request,uid,page):
    day_time = int(time.mktime(datetime.date.today().timetuple()))
    skipnum = (page - 1) * 50
    rebatelogs=models.rebatelog.objects(parentid=uid,addTime__gte=day_time).skip(skipnum).limit(50).order_by('-addTime')
    rdata=[]
    for rebatelog in rebatelogs:
        rdata.append({'childId':rebatelog.uid,'price':rebatelog.price,'rebatechip':rebatelog.rebatechip,'lev':rebatelog.lev})
    return JsonResponse({'errno':errorDefine.SUCCESS,
                         'datas':rdata})
#查询领取金币日志
def queryChipLog(request,uid,page):
    exteninfo = models.extensionRelation.objects(_id=uid).first()
    if not exteninfo:
        exteninfo = models.extensionRelation(_id=uid, parents=[], childs=[])
        exteninfo.save()
    tolRecv = exteninfo.tolRecv
    skipnum = (page - 1) * 50
    nchiplogs=models.nchiplog.objects(uid=uid).skip(skipnum).limit(50).order_by('-timestamp')
    rdata = []
    for nchiplog in nchiplogs:
        rdata.append({'uid': nchiplog.uid, 'todayFlowingChips': nchiplog.todayFlowingChips, 'timestamp':time.strftime("%Y/%m/%d %H:%M:%S",time.localtime(nchiplog.timestamp))})
    return JsonResponse({'errno':errorDefine.SUCCESS,
                         'tolRecv':tolRecv,
                         'datas':rdata})
#查询每日数据日志
def queryCurDayInfo(request,uid,page):
    daystr = time.strftime("%Y%m%d", time.localtime())
    skipnum = (page - 1) * 50
    nchiplogs= models.rebateItem.objects(uid=uid,lastupdatetime=daystr).skip(skipnum).limit(50).order_by('-todayrebatetchip')
    rdata = []
    for nchiplog in nchiplogs:
        rdata.append({'uid':nchiplog.childId,'todaytchip':nchiplog.todaytchip,'todayrebatetchip':nchiplog.todayrebatetchip,'todaybetchip':nchiplog.todaybetchip,'todaytbetchip':nchiplog.todaytbetchip,'lev':nchiplog.lev})
    return JsonResponse({
        'errno':errorDefine.SUCCESS,
        'datas':rdata,
    })
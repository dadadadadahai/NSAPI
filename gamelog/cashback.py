#返利相关记录查询
from django.http import JsonResponse
from . import models
#查询首页概要信息
def getIndexData(request,uid):
    #直属下级人数
    belowNum =  models.rebateItem.objects(uid=uid,lev=1).count()
    validinviteoj = models.validinvite.objects(_id=uid).first()
    res={
        'belowNum':belowNum,   #下线人数
        'validinViteNewPlayerNum':0, #未领取返利新用户人数
        'validinViteNewPlayerChips':0,#邀请新用户返利总额
        'validinViteActivePlayerNum':0,#未领取返利的用户人数
        'validinViteActivePlayerChips':0,#累计活跃用户返利
        'validinViteRechargePlayerRechargeChips':0,#未领取返利充值总金额
        'validinViteRechargePlayerChips':0#累计充值总金额带来的返利
    }
    if validinviteoj is not None:
        res['validinViteNewPlayerNum']=validinviteoj['validinViteNewPlayerNum']
        res['validinViteNewPlayerChips']=validinviteoj['validinViteNewPlayerChips']
        res['validinViteActivePlayerNum']=validinviteoj['validinViteActivePlayerNum']
        res['validinViteActivePlayerChips']=validinviteoj['validinViteActivePlayerChips']
        res['validinViteRechargePlayerRechargeChips']=validinviteoj['validinViteRechargePlayerRechargeChips']
        res['validinViteRechargePlayerChips'] = validinviteoj['validinViteRechargePlayerChips']
    return JsonResponse(res,safe=False)

#根据时间范围筛选记录
def getTimeRandData(request,uid,sTime,eTime):
    res={
        'fNum':0,#首充数量
        'fMoney':0,#首充金额
        'oNum':0,#充值数量
        'oMoney':0,#充值金额
        'bPeopleNum':0,#下注人数
        'bPeopleMoney':0#下注金额
    }
    #首充处理
    firstPipeline =[
        {'$match': {'uid': uid, 'lev': 1}},
        {'$lookup': {'from':'rechargeinfo','localField': 'childId','foreignField': '_id','as':'rechargeinfo'}},
        {'$unwind': '$rechargeinfo'},
        {'$match': {'$and':[{'rechargeinfo.discountInfo.firstBuyTime': {'$gte': sTime}}, {'rechargeinfo.discountInfo.firstBuyTime': {'$lt': eTime}}]}},
        {'$group': {'_id': 'null', 'fNum': {'$sum': 1}, 'fMoney': {'$sum': '$rechargeinfo.discountInfo.firstMoney'}}}
    ]
    result = models.rebateItem.objects().aggregate(firstPipeline)
    for f in result:
        res['fNum']=f['fNum']
        res['fMoney']=f['fMoney']
        break
    #计算充值数量 充值金额 下注人数 下注金额
    chargeAndBetPipeline=[
        {'$match':  {'$and':[{'dayTimeStamp': {'$gte': sTime}},{'dayTimeStamp': {'$lt': eTime}},{'parent': uid}]}},
        # {'$group': {'_id': 'null','betNum': {'$sum': '$betNum'}, 'chargeNum': {'$sum': '$chargeNum'}, 'chargeMoney': {'$sum': '$chargeMoney'}, 'betChip': {'$sum': '$betChip'}}}
        {'$group': {'_id': 'null', 'chargeMoney': {'$sum': '$chargeMoney'}, 'betChip': {'$sum': '$betChip'}}}
    ]
    chargeAndBetPipeRes = models.curBetCharge_Record.objects().aggregate(chargeAndBetPipeline)
    for f in chargeAndBetPipeRes:
        # res['oNum'] = f['chargeNum']
        res['oMoney'] = f['chargeMoney']
        # res['bPeopleNum'] = f['betNum']
        res['bPeopleMoney'] = f['betChip']
        break
    #统计充值人数和下注人数
    chargeAndBetPNumPipeline = [
        # {'$match': {'dayTimeStamp': {'$gte': sTime}, 'dayTimeStamp': {'$lte': eTime}, 'parent': uid,'chargeNum':{'$gt':0}}},
        {'$match': {'$and': [{'dayTimeStamp': {'$gte': sTime}}, {'dayTimeStamp': {'$lt': eTime}}, {'parent': uid},{'chargeNum':{'$gt':0}}]}},
        {'$group':{'_id':'$uid'}},
        {'$count':'cum'}
    ]
    chargeAndBetPNumPipelineres = models.curBetCharge_Record.objects().aggregate(chargeAndBetPNumPipeline)
    for f in chargeAndBetPNumPipelineres:
        res['oNum'] = f['cum']
        # res['bPeopleNum'] = f['betNum']
        break
    chargeAndBetPNumPipelineqt = [
        {'$match': {'$and': [{'dayTimeStamp': {'$gte': sTime}}, {'dayTimeStamp': {'$lt': eTime}}, {'parent': uid},{'betNum':{'$gt':0}}]}},
        {'$group':{'_id':'$uid'}},
        {'$count': 'bNum'}
    ]
    chargeAndBetPNumPipelineresqt=models.curBetCharge_Record.objects().aggregate(chargeAndBetPNumPipelineqt)
    for fq in chargeAndBetPNumPipelineresqt:
        res['bPeopleNum'] = fq['bNum']
        break
    return JsonResponse(res,safe=False)
#查询返利明细,下级的充值明细,押注明细
#查询
#curBetCharge_Record
def getTimeRandDetailData(request,uid,curPage,sTime,eTime):
    maxPage=10
    res=[]
    result = models.curBetCharge_Record.objects(dayTimeStamp__gte=sTime,dayTimeStamp__lt=eTime,parent=uid).order_by('-chargeMoney').skip(curPage*maxPage).limit(maxPage)
    for r in result:
        res.append({
            'dayTimeStamp':r['dayTimeStamp'], #0点时间戳
            'uid':r['uid'],     #用户id
            'betChip':r['betChip'], #用户下注值
            'chargeMoney':r['chargeMoney'],#用户充值值
        })
    return JsonResponse(res,safe=False)

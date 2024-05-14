from django.http import JsonResponse
from . import models

levMap = {
    1: (1000, 199999, 10),
    2: (200000, 399999, 20),
    3: (400000, 799999, 30),
    4: (800000, 1599999, 40),
    5: (1600000, 3199999, 50),
    6: (3200000, 6399999, 60),
    7: (6400000, 11999999, 70),
    8: (12000000, 23999999, 80),
    9: (24000000, 49999999, 90),
    10: (50000000, 99999999, 100),
    11: (100000000, 149999999, 110),
    12: (150000000, 199999999, 120),
    13: (200000000, 299999999, 130),
    14: (300000000, 399999999, 140),
    15: (400000000, 499999999, 150),
    16: (500000000, 599999999, 160),
    17: (600000000, 699999999, 170),
    18: (700000000, 799999999, 180),
    19: (800000000, 999999999, 190),
    20: (1000000000, 99999999999, 200),
}

def getPro(chip):
    for lev in levMap:
        minChip = levMap[lev][0]
        maxChip = levMap[lev][1]
        if chip >= minChip and chip <= maxChip:
            return levMap[lev][2]
    return 0
def getTeamCashBack(request, uid):
    # 查询除rebateItem表
    res = {
        'lev': 0,
        'allTeamNum': 1,  # 所有团队成员数量
        'belowNum': 0,  # 直属下级数量
        'todaybetchip': 0,  # 当日总下注
        'todaytbetchip': 0 , # 当日总返利
        'amountavailablechip':0 #可领取佣金金额
    }
    exModel =  models.extensionRelation.objects(_id=uid).first()
    if exModel:
        todayBetAll = exModel['todayBetAll']
        for lev in levMap:
            minChip = levMap[lev][0]
            maxChip = levMap[lev][1]
            if todayBetAll>=minChip and todayBetAll<=maxChip:
                res['lev'] = lev
                break
        res['allTeamNum'] = models.rebateItem.objects(uid=uid).count()+1
        res['belowNum'] = models.rebateItem.objects(uid=uid,lev=1).count()
        if exModel['todayBetAll'] is not None:
            res['todaybetchip'] = exModel['todayBetAll']
        # if exModel['todayBetFall'] is not None:
        #     res['todaytbetchip'] = exModel['todayBetFall']
        pro = getPro(res['todaybetchip'])
        res['todaytbetchip'] = res['todaybetchip']*pro/10000
        if exModel['amountavailablechip'] is not None:
            res['amountavailablechip'] = exModel['amountavailablechip']
    #统计团队规模
    return JsonResponse(res,safe=False)
def getLowDetail(request,uid,curPage):
    pageNum = 12
    rebateItemPipeline=[
        {'$match': {'uid': uid}},
        {'$lookup': {'from':'extension_relation', 'localField': 'childId', 'foreignField': '_id', 'as':'extension_relation'}},
        {'$unwind': '$extension_relation'},
        {'$skip': curPage*pageNum},
        {'$limit': pageNum},
        {'$sort': {'extension_relation.todayBetAll': -1}},
        {
        '$project': {
            'childId': '$childId',
            'todaybetchip': '$extension_relation.todayBetAll',
            # 'todaytbetchip': '$extension_relation.todayBetFall',
        }
        }
    ]
    res=[]
    #执行查询
    result=models.rebateItem.objects().aggregate(rebateItemPipeline)
    for f in result:
        uid = f['childId']
        uinfo = models.userinfo.objects(_id=uid).first()
        todaybetchip = 0
        if 'todaybetchip' in f:
            todaybetchip=f['todaybetchip']
        # if 'todaytbetchip' in f:
        #     todaytbetchip = f['todaytbetchip']
        pro = getPro(todaybetchip)
        todaytbetchip =todaybetchip*pro/10000
        res.append({
            'nickname':uinfo.base.nickname, #用户昵称
            'headurl':uinfo.base.headurl,   #用户头像
            'todaybetchip':todaybetchip, #当日下注金币
            'todaytbetchip':todaytbetchip#当日返利金币
        })
    return JsonResponse(res,safe=False)

from django.shortcuts import render
from django.http import JsonResponse
from pprint import pprint
from . import models
# Create your views here.
def GetToltalGameRecord(request,uid,sTime,eTime):
    pipeLine = [
        {'$match': {'sTime': {'$gte': sTime, '$lte': eTime}, 'uid': uid}},
        {'$project': {'win': {'$subtract': ["$aChip", "$bChip"]}, 'betChip': "$betChip", 'gameId': "$gameId",
                      'bNum': {'$cond': {'if': {'$gt': ["$betChip", 0]}, 'then': 1, 'else': 0}}}},
        {'$group': {'_id': 'null', 'betCoin': {'$sum': "$betChip"}, 'winCoin': {'$sum': "$win"},
                    'betNum': {'$sum': "$bNum"}}},
    ]
    result = models.gameMatchLog.objects().aggregate(pipeLine)
    res={
        'totalBetNum':0,
        'totalBetCoin':0,
        'totalWinCoin':0
    }
    for single in result:
        res['totalBetNum']=single['betNum']
        res['totalBetCoin'] = single['betCoin']
        res['totalWinCoin'] = single['winCoin']
        break
    return JsonResponse(res)
def GetListGameRecord(request,uid,curPage,sTime,eTime):
    PageNum = 20
    pipeLine=[
        {'$match': {'sTime': {'$gte': sTime, '$lte': eTime}, 'uid': uid}},
        {'$project': {'win': {'$subtract': ["$aChip","$bChip"]}, 'betChip': "$betChip", 'gameId': "$gameId", 'bNum': {'$cond': { 'if':{'$gt': ["$betChip", 0]}, 'then': 1, 'else':0}},'sTime':'$sTime'}},
        {'$group': {'_id': '$gameId', 'betCoin': {'$sum': "$betChip"}, 'winCoin': {'$sum': "$win"}, 'betNum': {'$sum': "$bNum"},'sTime':{'$max':'$sTime'}}},
        {'$sort': {'sTime': -1}},
        {'$skip': curPage*PageNum},
        {'$limit': PageNum},
    ]
    result = models.gameMatchLog.objects().aggregate(pipeLine)
    resList=[]
    for res in result:
        resList.append(
            {
                'gameId':res['_id'],
                'totalBetNum' : res['betNum'],
                'totalBetCoin' : res['betCoin'],
                'totalWinCoin' : res['winCoin'],
            }
        )
    return  JsonResponse(resList,safe=False)
#查询游戏详细记录
def GetGameDetailList(request,uid,gameId,curPage,sTime,eTime):
    pageMax=20
    result = models.gameMatchLog.objects(gameId=gameId,uid=uid,sTime__gte=sTime,sTime__lte=eTime).skip(curPage*pageMax).limit(pageMax).order_by('-sTime')
    resList=[]
    for res in result:
        resList.append({
            'id':str(res['_id']),
            'winCoin':res['aChip']-res['bChip'],
            'betCoin':res['betChip'],
            'time':res['sTime']
        })
    return JsonResponse(resList,safe=False)
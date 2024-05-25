import time

from django.http import JsonResponse
from errorDefine import errorDefine
from . import models
# Create your views here.
def bind(request,parentInviter,uidInviter):
    if uidInviter==parentInviter:
        return JsonResponse({'errno':errorDefine.Param})
    if uidInviter==None or uidInviter=='':
        return JsonResponse({'errno':errorDefine.Param})
    parentinfo = models.userinfo.objects(base__inviteCode=parentInviter).first()
    if not parentinfo:
        return JsonResponse({'errno':errorDefine.NOUSER})
    parentId = parentinfo._id
    uinfos = models.userinfo.objects(base__inviteCode=uidInviter).first()
    if not uinfos:
        return JsonResponse({'errno': errorDefine.NOUSER})
    uid = uinfos._id
    result = bindById(parentId,uid)
    return JsonResponse(result)
#获取父推广关系信息
def getParentInfo(parentId):
    parentInfo=None
    parents = models.extensionRelation.objects(_id=parentId)
    if len(parents)<=0:
        parentInfo = models.extensionRelation(_id=parentId,parents=[],belowNum=0)
        parentInfo.save()
    else:
        parentInfo = parents[0]
    return parentInfo
def bindById(parentId,uid):
    #获取父级相关
    parentInfo=getParentInfo(parentId)
    relations = models.extensionRelation.objects(_id=uid)
    if len(relations)<=0:
        cparents=[]
        if parentId>0:
            parents = parentInfo.parents
            cparents = parents.copy()
            cparents.append(parentId)
            calcBelowNum(parentInfo)
            #直属下级+1
            parentInfo.oneUnderNum+=1
            parentInfo.save()
        #保存数据库
        trelation=models.extensionRelation(_id=uid,parents=cparents,parentsTime=time.time(),parent=parentId,belowNum=0)
        trelation.save()
    else:
        trelation = relations[0]
        cparents =trelation.parents
        if len(cparents)>0:
            return {'errno':errorDefine.ExistBindRelation}
        if models.rebateItem.objects(uid=uid,childId=parentId).first():
            return {'errno': errorDefine.Param}
        if parentId>0:
            parents = parentInfo.parents
            cparents =parents.copy()
            cparents.append(parentId)
            trelation.parents = cparents
            trelation.parent = parentId
            calcBelowNum(parentInfo)
            parentInfo.save()
        trelation.save()
    lev = 1
    index = len(trelation.parents)-1
    while True:
        if index<0 or lev>4:
            break
        chip = 0
        parentId = trelation.parents[index]
        models.rebateItem(uid=parentId,childId=uid,chip=chip,lev=lev,tchip=0,bindTime=time.time()).save()
        index = index -1
        lev = lev +  1
    #插入绑定关系表
    return {'errno':errorDefine.SUCCESS}
#计算下级人数统计
def calcBelowNum(parentInfo):
    parentInfo.belowNum =parentInfo.belowNum + 1
    parents = parentInfo.parents
    tmpParents = parents.copy()
    tmpParents = tmpParents[::-1]
    forward = 1
    for parentId in tmpParents:
        if forward>=4:
            break
        parent = models.extensionRelation.objects(_id=parentId).first()
        if parent:
            parent.belowNum = parent.belowNum + 1
            parent.save()
            forward = forward + 1
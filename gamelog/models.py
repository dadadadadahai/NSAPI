from django.db import models

# Create your models here.
from mongoengine import Document,fields,IntField,DictField,EmbeddedDocument,StringField,EmbeddedDocumentField,ListField,ObjectIdField

#定义gameMatchLog数据结构
class gameMatchLog(Document):
    _id=ObjectIdField()
    uid=IntField()
    table=StringField()
    tax=IntField()
    bChip=IntField() #下注前金额
    gameId=IntField() #下注后金额
    gameType=IntField() #游戏场次  忽略
    aChip=IntField()    #下注后金额
    sTime=IntField()   #保存时间
    betChip=IntField() #下注金额
    meta={
        'strict': False,
        'collection': 'gameMatchLog'
    }
class base(EmbeddedDocument):
    headurl = StringField()
    nickname=StringField()
    meta={
        'strict': False,
    }
class userinfo(Document):
    _id=IntField()
    base = EmbeddedDocumentField(base)
    meta={
        'strict': False,
    }
class rebateItem(Document):
    _id=ObjectIdField()
    uid=IntField()
    childId=IntField()
    lev = IntField()
    chip=IntField()
    tchip=IntField()
    betchip=IntField()
    tbetchip=IntField()
    todaytchip=IntField()
    todayrebatetchip=IntField()
    todaybetchip=IntField()
    todaytbetchip=IntField()

    meta = {
        'strict': False,
        'collection': 'rebateItem'
    }
class validinvite(Document):
    _id = IntField()
    #未领取返利新用户人数
    validinViteNewPlayerNum=IntField()
    #邀请新用户返利总额
    validinViteNewPlayerChips = IntField()
    #未领取返利的用户人数
    validinViteActivePlayerNum=IntField()
    #累计活跃用户返利
    validinViteActivePlayerChips=IntField()
    #未领取返利充值总金额
    validinViteRechargePlayerRechargeChips=IntField()
    #累计充值总金额带来的返利
    validinViteRechargePlayerChips=IntField()
    meta = {
        'strict': False,
        'collection': 'validinvite'
    }
class discountInfoItem(EmbeddedDocument):
    FirstBuyTime=IntField()
    meta={
        'strict': False,
    }
#查询首充结构体
class rechargeinfo(Document):
    _id=IntField()
    discountInfo=EmbeddedDocumentField(discountInfoItem)
    meta = {
        'strict': False,
        'collection': 'rechargeinfo'
    }

class curBetCharge_Record(Document):
    _id = ObjectIdField()
    dayTimeStamp=IntField()
    uid=IntField()
    parent=IntField()
    betChip=IntField()
    betNum=IntField()
    chargeMoney=IntField()
    chargeNum=IntField()
    meta = {
        'strict': False,
        'collection': 'curBetCharge_Record'
    }
class extensionRelation(Document):
    _id = IntField()  # 本人id
    todayBetAll=IntField(default=0)#今日团队下线金币下注
    todayBetFall=IntField(default=0)#今日总返利
    amountavailablechip=IntField(default=0) #可获得佣金金额
    meta = {
        'strict': False,
        'collection': 'extension_relation',
    }

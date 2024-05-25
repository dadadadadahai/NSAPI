
from mongoengine import Document,fields,IntField,DictField,EmbeddedDocument,StringField,EmbeddedDocumentField,ListField
# Create your models here.
#point 结构体
class point(EmbeddedDocument):
    validinViteList=ListField(IntField())
    meta={
        'strict': False,
    }
#用户模型
class base(EmbeddedDocument):
    phoneNbr=StringField()
    inviteCode =StringField()
    meta={
        'strict': False,
    }
class property(EmbeddedDocument):
    rebatechip=IntField()
    meta={
        'strict': False,
    }
class userinfo(Document):
    _id=IntField()
    base = EmbeddedDocumentField(base)
    property = EmbeddedDocumentField(property)
    point = EmbeddedDocumentField(point)
    meta={
        'strict': False,
    }
class exChildInfo(EmbeddedDocument):
    _id = IntField()
    addTime = IntField()
class rebatedetail(EmbeddedDocument):
    uid = IntField()
    lev = IntField()
    chip = IntField()
class extensionRelation(Document):
    _id=IntField()          #本人id
    parents = ListField(IntField())
    parent =IntField(default=0)         #直属上级id
    parentsTime=IntField(default=0)      #绑定时间
    # childs = ListField(EmbeddedDocumentField(exChildInfo))
    oneUnderNum = IntField(default=0)   #直属下线人数
    belowNum = IntField(default=0)       #下线总人数4层
    tolrebate = IntField(default=0)     #下线总共返利值
    rebatechip = IntField(default=0)  # 可提现金额
    tolBelowCharge = IntField(default=0) #下线总共充值
    todayFlowingChips =IntField(default=0) #当天可领取金额
    tomorrowFlowingChips = IntField(default=0)#明日可领取金额
    addFlowingTimes = IntField(default= 0) #上次添加金额的时间戳
    tolBetAll = IntField(default=0)#总押注
    tolBetFall=IntField(default=0)#总下注返金币
    tolRecv =IntField(default=0) #总领取
    freeValidinViteChips = IntField(default=0) #免费有效玩家可领取金额
    meta={
        'auto_create_index': False,
        'id_field': '_id',
        'strict': False,
        'collection':'extension_relation',
    }
class rebateItem(Document):
    uid=IntField()
    childId=IntField()
    chip=IntField()
    lev = IntField()
    tchip = IntField()
    bindTime=IntField()
    betchip=IntField(default=0)
    tbetchip=IntField(default=0)
    todaytchip = IntField(default=0)        #当日总充值
    todayrebatetchip = IntField(default=0)  #当日总充值返利
    todaybetchip =IntField(default=0) #当日总下注
    todaytbetchip = IntField(default=0) #当日总下注返利
    lastupdatetime = StringField() #数据更新时间
    meta={
        'collection':'rebateItem',
        'strict': False,
    }
class rebatelog(Document):
    uid = IntField()
    parentid = IntField()
    lev = IntField()
    price = IntField()
    rebatechip=IntField()
    addTime=IntField()
    meta={
        'collection':'rebatelog',
        'strict': False,
    }
class nchiplog(Document):
    uid=IntField()
    todayFlowingChips=IntField()
    timestamp=IntField()
    meta={
        'collection':'nchiplog',
        'strict': False,
    }
class validinvite(Document):
    _id = IntField()
    validinViteList = ListField(IntField())
    validinViteFreeList = ListField(IntField())
    validinViteNum = IntField(default=0)  #总邀请人数
    validinViteChips =IntField(default=0) #直返总金币
    meta={
        'collection':'validinvite',
        'strict': False,
    }
class validinvitelog(Document):
    uid=IntField()
    addChips=IntField()
    validinViteNum=IntField()
    addTime=IntField()
    childId=IntField()
    type=IntField()
    meta={
        'collection':'validinvitelog',
        'strict': False,
    }
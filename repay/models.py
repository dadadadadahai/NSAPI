from mongoengine import Document,fields,IntField,DictField,EmbeddedDocument,StringField,EmbeddedDocumentField,ListField
import time
# Create your models here.
class historyItem(EmbeddedDocument):
    hora    =  IntField()   #申请时间
    moedas = IntField()     #消耗的金币
    dinheiro =IntField() #实际体现值
    state   = IntField(default=1)    #状态 默认 1
#体现记录表
class withdrawcash(Document):
    _id = IntField() #玩家id
    serviceCharge = IntField()  #手续费
    refreshTime = IntField() #刷新时间
    statement   = IntField() #可提现金额
    cpf = StringField() #字符串,cpf账号
    name = StringField()#姓名
    chavePix = StringField()#账号
    flag    = IntField()
    history =ListField(EmbeddedDocumentField(historyItem))
    totalWithdrawal = IntField(default=0)#总体现金额
    withdrawcashNum = IntField(default=0)#今日兑换次数
    meta={
        'auto_create_index': False,
        'id_field': '_id',
        'strict': False,
        'collection':'withdrawcash'
    }
#代付订单表
class withdrawcash_order(Document):
    _id = IntField()
    uid = IntField()
    name = StringField()
    chavePix = StringField()
    cpf = StringField()
    timestamp = IntField()
    chavePixNum= IntField()  #0 CPF 1 PHONE 2 EMAIL
    moedas = IntField()
    dinheiro = IntField()
    times = StringField()
    state = IntField(default=1)
    orderId = StringField(default='') #平台订单id
    orderType=IntField()  #1 流水 2 返利
    paytype=StringField(default='')
    meta={
        'auto_create_index': False,
        'id_field': '_id',
        'strict': False,
        'collection':'withdrawcash_order',
        'ordering':['-_id'],
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
    meta={
        'strict': False,
    }
class withdrawcash(Document):
    _id=IntField()
    chavePix=StringField()
    name=StringField()
    flag = IntField()
    cpf = StringField()
    meta={
        'strict': False,
        'collection': 'withdrawcash',
    }
class exChildInfo(EmbeddedDocument):
    _id = IntField()
    addTime = IntField()

class extensionRelation(Document):
    _id=IntField()          #本人id
    parents = ListField(IntField())
    parentsTime=IntField(default=0)      #绑定时间
    childs = ListField(EmbeddedDocumentField(exChildInfo))
    rebatechip = IntField(default=0)  #可提现金额
    belowNum = IntField(default=0)       #下线总人数4层
    tolrebate = IntField(default=0)     #下线总共返利值
    tolBelowCharge = IntField(default=0) #下线总共充值
    tolCashOut = IntField(default=0)  #历史总提现
    meta={
        'auto_create_index': False,
        'id_field': '_id',
        'strict': False,
        'collection':'extension_relation',
    }


#生成订单唯一id
def CreateOrderUniqueId():
    id=0
    while True:
        id = int(round(time.time()*1000))
        if withdrawcash_order.objects(_id=id).first() is None:
            break
    return id
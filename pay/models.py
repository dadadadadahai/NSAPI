from mongoengine import Document,fields,IntField,DictField,EmbeddedDocument,StringField,EmbeddedDocumentField,ObjectIdField
import time
import random
from django.conf import settings
random.seed(time.time())
# Create your models here.
class base(EmbeddedDocument):
    regFlag = IntField()
    subplatid = IntField()
    adcode = StringField()
    meta={
        'strict': False,
    }
class userinfo(Document):
    _id=IntField()
    base = EmbeddedDocumentField(base)
    meta={
        'strict': False,
    }
#订单模型
class orderinfo(Document):
    #订单ID
    _id = StringField(required=True,unique=True)
    uid = IntField()
    #订单提交时间
    subTime = IntField()
    #商品id
    shopId = IntField()
    #提交金额
    subPrice = IntField()
    #fee手续费
    fee = IntField()
    #回调时间
    backTime = IntField()
    #回调金额
    backPrice = IntField()
    #支付方式
    payType = StringField()
    #支付平台,订单id
    order_no = StringField()
    #订单状态
    status = IntField()         #订单状态 0 已提交 1 成功
    isChip=IntField()
    #商品类型
    shopType = IntField()      #商品支付类型
    regFlag=IntField()
    subplatid = IntField()
    #click_id  订单产生时的click_id
    click_id = StringField()
    #记录像素值  辨别是哪个平台
    adcode = StringField()
    ip = StringField()
    fbc = StringField()
    fbp = StringField()
    #像素值
    pixelcode = StringField()
    HTTP_HOST = StringField(default='')
    meta={
        'auto_create_index': False,
        'id_field':'_id',
        'strict': False,
    }
#充值成功后添加到,返利处理表里面
class rebateFinal(Document):
    uid   = IntField()
    price = IntField()
    addTime = IntField()
    orderNo =StringField()
#生成订单唯一id
def CreateOrderUniqueId():
    id = ''
    while True:
        id = time.strftime('%Y%m%d%H%M%S',time.localtime())
        rvalTwo = random.randint(10,99)
        id = id + str(rvalTwo)
        prefix = settings.PREFIX
        if not prefix:
            prefix=''
        id = prefix + id
        if len(orderinfo.objects(_id=id))<=0:
            break
    return id
#用户渠道信息表
class uchannelinfo(Document):
    _id = IntField()            #用户id
    adcode = StringField()    #所属渠道
    click_id = StringField(default='')  #快手点击id
    fbc   = StringField(default='')   #fb相关
    fbp = StringField(default='')   #fb相关
    pixelcode = StringField(default='')  #fb像素值
    HTTP_HOST = StringField(default='') #http_host
    IsFirst = IntField(default=0)   #0 首次付费
    meta={
        'auto_create_index': False,
        'id_field': '_id',
        'strict': False,
        'collection':'uchannelinfo',
    }
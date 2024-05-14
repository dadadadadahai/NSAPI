from mongoengine import Document,fields,IntField,DictField,EmbeddedDocument,StringField,EmbeddedDocumentField,ListField
import redis,json
from django.conf import settings
import redis
# GogalRedis_pool = redis.ConnectionPool(host=settings.REDISINFO['addr'],port =settings.REDISINFO['port'],max_connections=10)
#userinfo 操作
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

#改变玩家返利提现值
def ZeroUserRebatechip(uid):
    re_redis = redis.Redis(connection_pool=GogalRedis_pool)
    jsonstr = re_redis.hget('userinfo', uid)
    if jsonstr:
        #redis 有效,更新redis
        jsonobj = json.loads(jsonstr)
        jsonobj['property']['rebatechip'] = 0
        re_redis.hset('userinfo',uid,json.dumps(jsonobj))
    else:
        userinfo.objects(_id=uid).update(set__property__rebatechip=0)

#读取玩家的可提现值

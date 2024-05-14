from mongoengine import Document,fields,IntField,DictField,EmbeddedDocument,StringField,EmbeddedDocumentField,ListField
from django.db import models

# Create your models here.
#用户模型
class base(EmbeddedDocument):
    phoneNbr=StringField()
    inviteCode =StringField()
    adjustId = StringField()            #adjust唯一标志
    regFlag =IntField()
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
class adidlog(Document):
    _id=StringField()
    postData = StringField()
    openView=StringField()
class mechineArray(Document):
    _id=StringField()
    meta={
        'strict': False,
        'collection':'mechine_array',
    }
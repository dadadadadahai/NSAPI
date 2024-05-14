from django.db import models

# Create your models here.
from mongoengine import Document,fields,IntField,DictField,EmbeddedDocument,StringField,EmbeddedDocumentField,ListField
class base(EmbeddedDocument):
    uploadFlag=IntField()
    meta={
        'strict': False,
    }
class userinfo(Document):
    _id=IntField()
    base = EmbeddedDocumentField(base)
    meta={
        'strict': False,
    }
class userImageUpload(Document):
    _id = IntField()
    imgData = StringField()
    timestamp=IntField()
    status = IntField()
    uploadFlag =IntField()  #玩家是否已经上传过图片

class userImageAddDesktop(Document):
    _id = IntField()
    imgData = StringField()
    timestamp=IntField()
    status = IntField()
    uploadFlag =IntField()  #玩家是否已经上传过图片
    meta={
        'collection':'user_image_addDesktop'
    }
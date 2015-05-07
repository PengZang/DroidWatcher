#coding=utf-8
from mongoengine import *
from bson.json_util import default
from support.help import myErr
connect('DroidWatcher',host='localhost',port=5000)

class Feature(Document):
    label=IntField()
    basic=ListField(IntField())
    ref=StringField()
    train=BooleanField()
    
    def getVect(self,option='basic'):
        tmp=self._data
        if tmp.has_key(option):
            return tmp[option]
        else:
            return None
    def setVect(self,data,option='basic'):
        tmp=self._data
        tmp[option]=data
                

class Addition(Document):
    permissionList=ListField(DictField())
    serviceList=ListField(StringField())
    activityList=ListField(StringField())
    receiverList=ListField(StringField())
    providerList=ListField(StringField())
    apiList=ListField(StringField())
    ref=StringField()
    

class Application(Document):
    name=StringField(default='UnKnown')
    md5=StringField(default='UnKnown')
    package=StringField()
    version=StringField(default='UnKnown')
    type=IntField()
    maxSDK=StringField(default='UnKnown')
    minSDK=StringField(default='UnKnown')
    targetSDK=StringField(default='UnKnown')

    

    signName=StringField(default='UnKnown')
#     signValue=StringField(default='UnKnown')

    certIssuer=StringField(default='UnKnown')
    rootTrusted=BooleanField(default=False)
    selfSigned=BooleanField(default=True)
    verifySign=BooleanField(default=False)
    subjectDN=StringField(default='UnKnown')

    
    mainActivity=StringField(default='Unknown')
    
    modifyDate=StringField()
    publicationDate=StringField()

    level=IntField()
    desc=StringField()
    hrefList=ListField(URLField())
    
    meta = {'indexes': [
        {'fields': ['$name', "$package"],
         'default_language': 'english',
         'weight': {'name': 1, 'package': 1}
        }
    ]}
    
    def toDict(self):
        tmp=self._data
        if tmp.has_key('id'):
            tmp['id']=str(tmp['id'])
        return tmp
        
    
    def fromDict(self,src):
        if not src.has_key('md5'):
            raise myErr('MD5值是必须指定的')
        if not src.has_key('name'):
            raise myErr('应用名称不能缺省')
        if not src.has_key('package'):
            raise myErr('包名称不能缺省')
        for key in src.keys():
            if key=='id':
                continue
            self._data[key]=src[key]
    
class Exp(Document):
    path=StringField(required=True)
    feature=ListField(IntField())
    train=BooleanField(default=False)
    label=IntField()
    match=IntField(default=None)
#     result=IntField(default=0)


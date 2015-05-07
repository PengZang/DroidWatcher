#coding=utf-8
import datetime
# sys.path.append('..')
from util import constant
from handle.extractor import Extractor
Collection=constant.fetchDB()['Application']
class Application:
    def __init__(self,obj={}):
        self.doc=obj

    # 数据库操作
    def update(self):
        result={"success":True,"msg":"数据库错误，稍后再试","data":None}
        keyword={"_id":self.doc['_id']} if self.doc.has_key('_id') else {"md5":self.doc["md5"]}
        self.set(['date','last'],datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        tmp=Collection.update(keyword,{"$set":self.doc},upsert=True)
        if tmp['ok']:
            result['success']=True
            if tmp['updatedExisting']:
                result['index']=keyword['_id'] if keyword.has_key('_id') else None
            else:
                result['index']=self.doc["_id"]=tmp['upserted']
        else:
            result['success']=False
        return result

    def insert(self):
        result={"success":True,"msg":"数据库错误，稍后再试","data":None}
        if Collection.find_one({'md5':self.doc['md5']}):
            result['success']=False
            result['msg']="该应用已经存在"
        else:
            self.set(['date','last'],datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            tmp=Collection.insert(self.doc)
            result['index']=self.doc["_id"]=tmp;result['success']=True
        return result

    def delete(self):
        result={"success":True,"msg":"数据库错误，稍后再试","data":None}
        keyword={"_id":self.doc['_id']} if self.doc.has_key('_id') else {"md5":self.doc["md5"]}
        tmp=Collection.remove(keyword)
        if not tmp['ok']:
            result['success']=False
        return result


    # 基本get/set操作包装
    def get(self,keyList):
        tmp=self.doc
        try:
            for key in keyList:
                tmp=tmp[key]
        except:
            return None
        return tmp

    def set(self,keyList,value):
        tmp=self.doc
        try:
            for i in range(0,len(keyList)-1):
                tmp=tmp[keyList[i]]
        except:
            return False
        tmp[keyList[-1]]=value
        return True


    # 一些初始整合操作
    def initialize(self,ex=None,path=None):
        if not ex and path:
            ex=Extractor(path)
        self.doc={}
        ex.extractAll(self)
        return True


    # 特征相关操作

    def getFeature(self):
        result={"success":True,"msg":"数据库错误，稍后再试","data":None}
        return result

    def setFeature(self,feature):
        result={"success":True,"msg":"数据库错误，稍后再试","data":None}
        return result

    def format(self):
        result={"success":True,"msg":""}
        if not self.doc.has_key('date'):
            self.doc['date']={}
        return result

    def abstract(self):
        tmp=self.doc.copy()
        rmList=['feature','_id']
        map(lambda x:tmp.pop(x) if tmp.has_key(x) else None,rmList)
        return tmp




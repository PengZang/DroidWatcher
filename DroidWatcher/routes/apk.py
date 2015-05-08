#coding=utf-8
import os,json,sys,io,traceback
from handle.schema import Application,Addition,Feature
from support.help import (myErr,Config,calMD5,saveFile, MSG)
from django.template.context_processors import request
from django.http.response import Http404, HttpResponse, JsonResponse
from hashlib import md5
from handle.extractor import Extractor, extractorFactory
from handle.generator import Generator, generatorFactory, GeneratorBriedge
from handle.detection import DetectorFactory, DetectorBriedge

    
def search(request):
    if not request.method=='POST':
        raise Http404
    req=json.loads(request.body)
    tmp=Application.objects.search_text(req['keyword'])
    apkList=map(lambda x:{
                          "name":x.name,
                          "version":x.version,
                          "md5":x.md5,
                          "modifyDate":x.modifyDate,
                          "publicationDate":x.publicationDate,
                          "id":str(x.id)
                          }, tmp)
    return JsonResponse({
                         "success":True,
                         "data":apkList,
                         "msg":''
                         })



def select(request):
    if not request.method=='POST':
        raise Http404
    req=json.loads(request.body)

    try:
        if not req.has_key('id'):
            raise myErr('请先选择应用')
        tmp=Application.objects(id=req['id']).first()
        if not tmp:
            raise myErr('错误的选择，没有该应用')
        current=tmp.toDict()
        request.session['apkId']=current['id']
    except myErr,e:
        return JsonResponse({
                             "success":False,
                             "data":None,
                             "msg":e.msg
                             })
    except Exception,e:
        return JsonResponse({
                             "success":False,
                             "data":None,
                             "msg":"后台错误，请稍后再试"
                             })
    else:
        return JsonResponse({
                             "success":True,
                             "data":current,
                             "msg":''
                             })




def upload(request):
    if not request.method=='POST':
        raise Http404
    try:
        tmpFile=request.FILES.get('file')
        if not tmpFile:
            raise myErr('未找到上传文件')
        if tmpFile.name.split('.')[-1]!='apk':
            raise myErr('不支持的文件格式')
        filePath=os.path.join(Config.UPLOAD,tmpFile.name)
        saveFile(tmpFile, filePath)
        md5=calMD5(filePath)
    except myErr,e:
        return JsonResponse({
                             "success":False,
                             "data":None,
                             "msg":e.msg
                             })
    except Exception,e:
        print(e.message)
        return JsonResponse({
                             "success":False,
                             "data":None,
                             "msg":"后台错误，请稍后再试"
                             })
    else:
        return JsonResponse({
                             "success":True,
                             "data":{
                                     "path":filePath,
                                     "md5":md5
                                     },
                             "msg":''
                             })
    


def record(request):
    if not request.method=='POST':
        raise Http404
#     req=json.loads(request.body)
    try:
        tmpReport=request.FILES.get('file')
        if not tmpReport:
            raise myErr('未接收到文件')
        if not tmpReport.name.split('.')[-1]=='json':
            raise myErr('非法的文件后缀名')
        context=json.loads(tmpReport.read())
        if Application.objects(md5=context['md5']).count()>0:
            raise myErr('该应用已存在，不可重复添加')
        app=Application()
        app.fromDict(context)
        app.type=2
        if not app.level:
            raise myErr('请指定应用的风险等级')
        app.save()
        request.session['apkId']=str(app.id)
        context['id']=str(app.id)
    except myErr,e:
        return JsonResponse({
                         "success":False,
                         "data":None,
                         "msg":e.msg
                         })
    except Exception,e:
        return JsonResponse({
                         "success":False,
                         "data":None,
                         "msg":"后台错误，请稍后再试"
                         })
    else:
        return JsonResponse({
                             "success":True,
                             "data":context,
                             "msg":""
                             })

def process(request):
    if not request.method=='POST':
        raise Http404
    req=json.loads(request.body)
    try:
        if not req.has_key('md5'):
            raise myErr('请指定MD5值')
        app=Application.objects(md5=req['md5']).first()
        MSG[req['md5']]=[]
        if app:
            request.session['apkId']=str(app.id)
            raise myErr('该应用已存在，可直接查看')
        if not os.path.exists(req['path']):
            raise myErr('请先提交APK文件')
        if not req['type'] in [0,1]:
            raise myErr('不支持的样本类型')
        ex=extractorFactory(Config.EXTRACT,req['path'])
        app=Application()
        app.fromDict(ex.extractBasicInfo())
        if not app.md5==req['md5']:
            raise myErr('MD5值有误')
        MSG[app.md5].append('<p>APK基本信息提取完成</p>')
        
        
        add=Addition()
        add._data=ex.extractAddition()
        ge=generatorFactory(Config.FEATURE)
        MSG[app.md5].append('<p>APK初步分析完毕</p>')
        
        fea=Feature()
        fea.setVect(ge.generateFeature(add._data),Config.FEATURE)
        MSG[app.md5].append('<p>特征提取完毕</p>')
        
        if req['type']==0:
            app.type=0
            if not req.has_key('level'):
                raise myErr('请指定训练样本的风险等级')
            if req['level']>4 or req['level']<0:
                raise myErr('不支持的风险等级')
            app.level=req['level']
            fea.label=1 if app.level>0 else 0
            fea.train=True
            
        
        else:
            app.type=1
            fea.train=False
            print(Config.METHOD)
            detector=DetectorFactory(Config.METHOD)
            tmp=detector.detect({
                             "match":ex.apk,
                             "default":fea.getVect(Config.FEATURE)
                             })
            app.level=tmp
            fea.label=1 if tmp>0 else 0
            MSG[app.md5].append('<p>APK恶意风险等级判定完毕</p>')
        
            
    except myErr,e:
        print traceback.format_exc()
        res={
             "success":False,
             "data":None,
             "msg":e.msg
             }
    except Exception,e:
        print traceback.format_exc()
        res={
             "success":False,
             "data":None,
             "msg":"后台错误，请稍后再试"
            }
    else:
        print 'SUCCESS'
        res={
             "success":True,
             "data":None,
             "msg":""
             }
    
    try:
        if res['success']:
            app.save()
            add.ref=fea.ref=request.session['apkId']=str(app.id)
            add.save()
            fea.save()
            res.data=app.toDict()
        del MSG[req['md5']],ex,ge,detector
    finally:
        return JsonResponse(res)   


def processNew(request):
    if not request.method=='POST':
        raise Http404
    req=json.loads(request.body)
    try:
        if not req.has_key('md5'):
            raise myErr('请指定MD5值')
        app=Application.objects(md5=req['md5']).first()
        MSG[req['md5']]=[]
        if app:
            request.session['apkId']=str(app.id)
            raise myErr('该应用已存在，可直接查看')
        if not os.path.exists(req['path']):
            raise myErr('请先提交APK文件')
        if not req['type'] in [0,1]:
            raise myErr('不支持的样本类型')
        ex=extractorFactory(Config.EXTRACT,req['path'])
        app=Application()
        app.fromDict(ex.extractBasicInfo())
        if not app.md5==req['md5']:
            raise myErr('MD5值有误')
        MSG[app.md5].append('<p>APK基本信息提取完成</p>')
        
        
        add=Addition()
        add._data=ex.extractAddition()
        ge=GeneratorBriedge(Config.FEATURE_LIST,add._data)
        MSG[app.md5].append('<p>APK初步分析完毕</p>')
        
        fea=Feature()
        fea._data=ge.generateAll()
        MSG[app.md5].append('<p>特征提取完毕</p>')
        
        if req['type']==0:
            app.type=0
            if not req.has_key('level'):
                raise myErr('请指定训练样本的风险等级')
            if req['level']>4 or req['level']<0:
                raise myErr('不支持的风险等级')
            app.level=req['level']
            fea.label=1 if app.level>0 else 0
            fea.train=True
            
        
        else:
            app.type=1
            fea.train=False
            detector=DetectorBriedge(Config.METHOD_LIST)
            tmp=detector.run({
                             "match":ex.apk,
                             "default":fea.getVect(Config.FEATURE)
                             })
            app.level=tmp
            fea.label=1 if tmp>0 else 0
            MSG[app.md5].append('<p>APK恶意风险等级判定完毕</p>')
        
            
    except myErr,e:
        print traceback.format_exc()
        res={
             "success":False,
             "data":None,
             "msg":e.msg
             }
    except Exception,e:
        print traceback.format_exc()
        res={
             "success":False,
             "data":None,
             "msg":"后台错误，请稍后再试"
            }
    else:
        print 'SUCCESS'
        res={
             "success":True,
             "data":None,
             "msg":""
             }
    
    try:
        if res['success']:
            app.save()
            add.ref=fea.ref=request.session['apkId']=str(app.id)
            add.save()
            fea.save()
            res.data=app.toDict()
        del MSG[req['md5']],ex,ge,detector
    finally:
        return JsonResponse(res)
    


def query(request):
    if not request.method=='POST':
        raise Http404
    req=json.loads(request.body)
    res=''
    try:
        md=req['md5']
        if MSG.has_key(md):
            res=' '.join(MSG[md])
            print(res)
        if res:
            MSG[md]=[]
    finally:
        return HttpResponse(res)   
        
            
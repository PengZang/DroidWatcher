#coding=utf-8
import os,json
from handle.schema import Application,Addition,Feature
from support.help import myErr, Config
from django.template.context_processors import request
from django.http.response import Http404, HttpResponse, JsonResponse

def basic(request):
    if not request.method=='GET':
        raise Http404
    apkId=request.session.get('apkId')
    try:
        tmp=Application.objects(id=apkId).first()
        if not tmp:
            raise myErr('不存在该应用')
        tmp=tmp.toDict()
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
                             "data":tmp,
                             "msg":''
                             })

def addition(request):
    if not request.method=='GET':
        raise Http404
    apkId=request.session.get('apkId')
    print apkId
    try:
        tmp=Addition.objects(ref=apkId).first()
        if not tmp:
            if Application.objects(id=apkId).count()==0:
                raise myErr('不存在此应用的记录')
            else:
                raise myErr('该应用并无附加的分析报告')
        tmp=tmp._data
        tmp['id']=str(tmp['id'])
    except myErr,e:
        return JsonResponse({
                             "success":False,
                             "data":None,
                             "msg":e.msg
                             })
    except Exception,e:
        print e
        return JsonResponse({
                             "success":False,
                             "data":None,
                             "msg":"后台错误，请稍后再试"
                             })
    else:
        return JsonResponse({
                             "success":True,
                             "data":tmp,
                             "msg":''
                             })
       
           


def edit(request):
    print 'HAHA'
    if not request.method=='POST':
        raise Http404
    req=json.loads(request.body)
    apkId=request.session.get('apkId')
    res={}
    try:
        if not req.has_key('operation'):
            raise myErr('请务必指定执行操作')
        if req['operation']=='delete':
            if not apkId:
                raise myErr('请先指定当前应用')
            Addition.objects(ref=apkId).delete()
            Feature.objects(ref=apkId).delete()
            Application.objects(id=apkId).delete()
            request.session['apkId']=None
        elif req['operation']=='modify':
            if not apkId:
                raise myErr('请先指定当前应用')
            app=Application(id=apkId)
            app.fromDict(req['data'])
            app.save()
            res=req['data']
        elif req['operation']=='create':
            app=Application()
            app.fromDict(req['data'])
            app.save()
            res=app.toDict()
            request.session['apkId']=str(app.id)
        else:
            raise myErr('不支持的操作类型')
    except myErr,e:
        return JsonResponse({
                         "success":False,
                         "data":None,
                         "msg":e.msg
                         })
    except Exception,e:
        print e.message
        return JsonResponse({
                         "success":False,
                         "data":None,
                         "msg":"后台错误，请稍后再试"
                         })
    else:
        return JsonResponse({
                             "success":True,
                             "data":res,
                             "msg":""
                             })
        
        


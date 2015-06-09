#coding=utf-8
import os,json
from handle.schema import Application,Addition,Feature
from support.help import myErr, Config,logger
from django.template.context_processors import request
from django.http.response import Http404, HttpResponse, JsonResponse
from offline.core import train

def editMethod(request):
    if  not request.method=='POST':
        raise Http404
    
    req=json.loads(request.body)
    try:
        print(Config.METHOD)
        if not req.has_key('method'):
            raise myErr('请指定选择的检测方法')
        if not req['method'] in Config.AVAILABLE_METHOD:
            raise myErr('不支持的检测方法')
        Config.METHOD=req['method']
        print(Config.METHOD)
    except myErr,e:
        logger.info(e.msg)
        return JsonResponse({
                         "success":False,
                         "data":None,
                         "msg":e.msg
                         })
    except Exception,e:
        logger.error(e.message)
        return JsonResponse({
                         "success":False,
                         "data":None,
                         "msg":"后台错误，请稍后再试"
                         })
    else:
        return JsonResponse({
                             "success":True,
                             "data":None,
                             "msg":""
                             })
    

def startTrain(request):
    if not request.method=='GET':
        raise Http404
    pid=os.fork()
    if pid==0:
        methods=Config.METHOD.split('+')
        for m in methods:
            train(m)
    else:
        logger.info('Train Process Startred')
        return JsonResponse({
                             "success":True,
                             "data":None,
                            "msg":""
                             })

        
def info(request):
    if not request.method=='GET':
        raise Http404
    res={}
    try:
        database={}
        database['total']=Application.objects.count()
        database['train']=Application.objects(type=0).count()
        database['test']=Application.objects(type=1).count()
        database['record']=Application.objects(type=2).count()
        database['ware']=Application.objects(level__gt=0).count()
        database['normal']=Application.objects(level=0).count()
        method={}
        method['available']=Config.AVAILABLE_METHOD
        method['current']=Config.METHOD
        res['database']=database;res['method']=method
    except Exception,e:
        logger.error(e.message)
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
    
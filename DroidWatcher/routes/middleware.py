#coding=utf-8
from django.http.response import JsonResponse, Http404

class SelectMiddleware(object):
    def process_request(self,request):
        url=request.get_full_path()
        if not url in ['/report/basic','/report/analysis']:
            return None
        apkId=request.session.get('apkId')
        if not apkId:
            if request.method=='POST':
                return JsonResponse({
                                 "success":False,
                                 "data":None,
                                 "msg":'请先指定当前应用'
                                 })
            else:
                raise Http404
        else:
            return None
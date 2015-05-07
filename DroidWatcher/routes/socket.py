#coding=utf-8
  
  
def rsocket(app):
    skt=SocketIO(app)

    @skt.on('req:apk')
    def on_apk(req):
        if not os.path.isfile(req['path']):
            emit('res:err',json.dumps({
                "success":False,
                "msg":"指定APK不存在",
                "data":None
            }))
            return
        ex=Extractor(req['path'])
        app=Application()
        try:
            app.initialize(ex)
            emit('res:process',json.dumps({
                "msg":"APK相关信息提取完毕..."
            }))
            app.set(['type'],req['type'])
            if req['malware']==1:
                app.set(['isMalware'],True)
            elif req['malware']==2:
                app.set(['isMalware'],False)
            tmp=app.insert()
            if not tmp.success:
                raise myErr(tmp.msg)
            emit('res:process',json.dumps({
                "msg":"APK存入数据库..."
            }))
            if not req['type']==constant.Type['Record']:
                feature=ex.generateFeature()
                emit('res:process',json.dumps({
                    "msg":"APK特征提取完毕..."
                }))
                tmp=app.setFeature(feature)
                if not tmp.success:
                    raise myErr(tmp.msg)
                if req['type']==constant.Type['Train']:
                    #训练过程
                    pass
                elif req['type']==constant.Type['Test']:
                    #测试过程
                    pass
                else:
                    raise myErr('所选应用类型不合法')

        except myErr as e:
            emit('res:err',json.dumps({
                "success":False,
                "msg":e.msg,
                "data":None
            }))
        else:
            emit('res:end',json.dumps({
                "success":True,
                "msg":"APK处理过程完毕",
                "data":str(app['doc']['_id'])
            }))
        os.remove(req['path'])
        return


    return skt



import os,sys
sys.path.append('.')
import pickle as pk
from handle.schema import Feature,Addition,Application
from handle.extractor import Extractor
from handle.generator import Generator
from lib.androguard.androguard.core import androconf
from sklearn import svm
from handle.trainer import trainerFactory

def isAPK(path):
    ret_type=androconf.is_android(path)
    return (ret_type=='APK')

def initDB(src,category):
    apkList=[]
    if os.path.isdir(src):
        for item in os.listdir(src):
            tmp=os.path.join(src,item)
            if isAPK(tmp):
                apkList.append(tmp)
    else:
        if isAPK(src):
            apkList.append(src)
    
    for item in apkList:
        try:    
            ex=Extractor(item)
            
            app=Application()
            app.fromDict(ex.extractBasicInfo())
            app.level=category
            app.type=0
            if Application.objects(md5=app.md5).count()>0:
                continue
            
            comset=Addition()
            comset._data=ex.extractAddition()
            
            
            ge=Generator()
            
            fset=Feature()
            fset.basic=ge.generateFeature(comset._data)
            fset.train=True
            fset.label= 1 if category >0 else 0
            app.save()
            comset.ref=fset.ref=str(app.id)
            comset.save()
            fset.save()
            print(item+' imported successfully!')
            del ex,ge,app,comset,fset
        except Exception,e:
            print e.message
            print('An error occured when import '+item+', will be discarded')
            continue
        
        
            
            
            
    

    
def train(method='svm',savePath=None,choice='basic'):
    if not savePath:
        savePath=os.path.abspath('./support/clf/'+method+'.pk')
    else:
        savePath=os.path.abspath(savePath)
    trainer=trainerFactory(method,choice,savePath)
    if not trainer:
        print('No such method to train for now')
        return
    trainer.train()
    trainer.save()
    print('Train Process Complete')



import io,logging
import pickle as pk
from lib.androguard.androguard.core import androconf
from hashlib import md5

MSG={}

logger=logging.getLogger('DroidWatcher')

def saveFile(src,path):
    dst=open(path,'wb')
    for chunk in src.chunks():
        dst.write(chunk)
    dst.close()
    
def calMD5(filePath):
    file=io.FileIO(filePath,'r')
    m=md5()
    bytes=file.read(1024)
    while(bytes!=b''):
        m.update(bytes)
        bytes=file.read(1024)
    file.close()
    return m.hexdigest() 

def isAPK(path):
    ret_type=androconf.is_android(path)
    return (ret_type=='APK')

class Config:
    ROOT='/Users/suemi/Workspace/DroidWatcher/'
    SUPPORT=ROOT+'support/'
    AAPT=SUPPORT+'tool/AAPT'
#     Method2Feature={
#                     "svm":"basic",
#                     "randomForest":'basic',
#                     "match":"apk"
#                     }
#     METHOD=['match','svm']
#     FEATURE=list(set([Method2Feature[x] for x in METHOD]))
#     Feature2Extractor={
#                        "basic":"basic",
#                        "apk":"basic"
#                        }
#     EXTRACTOR=list(set([ Feature2Extractor[x] for x in FEATURE]))
    AVAILABLE_METHOD=['match','svm','match+svm','randomForest','svm+randomForest']
    METHOD='svm+randomForest'
    METHOD_LIST=['svm','randomForest']
    FEATURE='basic'
    FEATURE_LIST=['basic']
    EXTRACT='basic'
    UPLOAD=SUPPORT+'upload/'
    permission=pk.load(open(SUPPORT+'cache/permission.pk','r'))
    SigDatabase=SUPPORT+'signatures/dbandroguard'
    SigConfig=SUPPORT+'signatures/dbconfig'
    SigDebug=False

class myErr(Exception):
    def __init__(self,msg):
        self.msg=msg;
    def __str__(self):
        return repr(self.msg)
#coding=utf-8
import datetime
import sys,os,base64,io
import subprocess as sub
from hashlib import md5
from lib.androguard.androguard.core.bytecodes import dvm
import lib.androguard.androguard.core.bytecodes.apk as ANG
from lib.androguard.androguard.core.analysis import analysis
from support.help import (Config,isAPK,myErr)


DEFAULT_SIGNATURE = analysis.SIGNATURE_L0_4

def contain(src,dst):
    tmp=src.split('->')[0].split('/')[0]
    mname=src.split('->')[1].split('(')[0]
    if not tmp=='Landroid':
        return False
    if '<' in mname:
        return False
    for item in dst:
        if item in src.lower():
            return True
    return False
            

class BasicExtractor:
    def __init__(self,filePath):
        self.filePath=filePath
    
    def extractAll(self):
        pass

class Extractor(BasicExtractor):
    def __init__(self,filePath):
        if not isAPK(filePath):
            raise myErr('并非APK文件')
        self.apk=ANG.APK(filePath)
        self.dex=dvm.DalvikVMFormat(self.apk.get_dex())
        self.vmx=analysis.VMAnalysis(self.dex)
        self.filePath=filePath
    
    
    def calMD5(self):
        myfile=io.FileIO(self.filePath,'r')
        m=md5()
        mybytes=myfile.read(1024)
        while(mybytes!=b''):
            m.update(mybytes)
            mybytes=myfile.read(1024)
        myfile.close()
        return m.hexdigest()

    def extractBasicInfo(self):
        app=self.apk;dst={}
        if not app.is_valid_APK():
            return False
        
        # Get name
        tmp=sub.check_output(Config.AAPT+' dump badging '+app.get_filename()+
                             ' | grep application-label:',shell=True)
        tmp=tmp.split('\'')[1] if tmp else 'UnKnown'
        dst['name']=tmp
        
        # Get MD5 Value
        dst['md5']=self.calMD5()
        
        # Get package
        dst['package']=app.get_package()
        
        # Get Version Information
        tmp = app.get_androidversion_name()
        dst['version']=tmp if tmp else 'UnKnown'
        
        # Get SDK Information
        tmp = app.get_max_sdk_version()
        dst['maxSDK'] = tmp if tmp else 'UnKnown'
        tmp=app.get_min_sdk_version()
        dst['minSDK'] = tmp if tmp else 'UnKnown'
        tmp=app.get_target_sdk_version()
        dst['targetSDK'] = tmp if tmp else 'UnKnown'

        # Get The Signature Information
        dst['signName']=app.get_signature_name()
#         dst['signValue']=app.get_signature()

        # Get The Certificate Information
        tmp= app.get_certificate(dst['signName'])
        if tmp[0]:
            cert=tmp[1]
            tmp=cert.issuerDN()
            dst['certIssuer']=tmp if tmp else 'UnKnown'
            dst['rootTrusted']=cert.get_TrustedRoot()
            dst['selfSigned']=cert.get_SelfSigned()
            dst['verifySign']=cert.get_SignatureVerified()
            tmp=cert.subjectDN()
            dst['subjectDN']=tmp if tmp else 'UnKnown'
        
        # Get Main Activity
        dst['mainActivity']=app.get_main_activity()

        # Set Date Information
        tmp = datetime.datetime.now()
        dst['modifyDate'] = tmp.strftime('%Y-%m-%d %H:%M:%S')
        tmp=datetime.datetime.strptime(cert.validFromStr(),'%a, %d %b %Y %H:%M:%S GMT')
        dst['publicationDate']=tmp.strftime('%Y-%m-%d %H:%M:%S')
        return dst

    def extractPermission(self):
        app=self.apk;dst=[]
        tmp=app.get_details_permissions()
        for key in tmp.keys():
            value=tmp[key]
            dst.append({
                        "name":key.split('.')[-1],
                        "level":value[0],
                        "desc":value[1],
                        "detail":value[2]
                        })
        del tmp
        return dst
    
#     def extractAPI(self):
#         res=[]
#         for m in self.dex.get_methods():
#             res.append(m.class_name+m.name)
#         return res
    
    def extractAPI(self):
        dex=self.dex
        apiList=[]
        for method in dex.get_methods():
            for i in method.get_instructions():
                if i.get_name()[:6]=='invoke':
                    call = i.get_output(0).split(',')[-1].strip()
                    call = call[:call.index(')')+1]
                    call=call.replace(';','')
                    call=call.split('(')[0]
                    if contain(call, ['sms','telephony','net','camera','graphics','bluetooth','location']):
                        apiList.append(call)
        apiList=list(set(apiList))
        return apiList

    def extractAddition(self):
        app=self.apk;dst={}
        dst['permissionList']=self.extractPermission()
        dst['serviceList']=app.get_services()
        dst['activityList']=app.get_activities()
        dst['receiverList']=app.get_receivers()
        dst['providerList']=app.get_providers()
        dst['apiList']=self.extractAPI()
        return dst

    

    def extractCFG(self):
        d=self.dex;x=self.vmx;res=''
        for method in d.get_methods():
            g = x.get_method(method)
            m=method.get_descriptor()
            if m==None:
                continue
            z_tmp=x.get_method_signature(method, predef_sign = DEFAULT_SIGNATURE).get_string()
            z_tmp = base64.b64encode( z_tmp )
            if len(z_tmp)>100:
                res+=z_tmp
        return res

    def extractAll(self):
        return self.extractBasicInfo(),self.extractAddition()


def extractorFactory(name,filePath):
    if name=='basic' :
        return Extractor(filePath)
    else:
        return None
    
    
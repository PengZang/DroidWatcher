from support.help import Config
from lib.androguard.elsim.elsim.elsign import dalvik_elsign 
import pickle as pk


class Detector:
    def __init__(self,clf=None):
        self.clf=clf
    
    def detect(self):
        pass
    
class MatchDetecor(Detector):
    database=Config.SigDatabase
    config=Config.SigConfig
    debug=Config.SigDebug
    def __init__(self,clf=None):
        if not clf:
            self.clf=dalvik_elsign.MSignature(MatchDetecor.database,MatchDetecor.config,
                                              MatchDetecor.debug,ps=dalvik_elsign.PublicSignature)
        else:
            self.clf=clf
            
    def detect(self,apk):
        ret=self.clf.check_apk(apk)
        if not ret[0]:
            return 0
        else:
            tmp=[x[1] for x in ret[1]]
            score=min(tmp)
            if score<0.1:
                return 3
            if score<0.2:
                return 2
            if score<0.3:
                return 1
 
    
class SVMDetecor(Detector):
    def __init__(self,clf=None):
        if not clf:
            self.clf=pk.load(open(Config.SUPPORT+'cache/svm.pk','r'))
        else:
            self.clf=clf
        
    def detect(self,x):
        return self.clf.predict([x])[0]
 
    
class RFDetecor(Detector):
    def __init__(self,clf=None):
        if not clf:
            self.clf=pk.load(open(Config.SUPPORT+'cache/randomForest.pk','r'))
        else:
            self.clf=clf
        
    def detect(self,x):
        return self.clf.predict([x])[0]

    
class Match_SVM(Detector):
    def __init__(self,clf={}):
        self.clf=clf if clf else {}
        if not self.clf.has_key('match'):
            self.clf['match']=None
        if not self.clf.has_key('svm'):
            self.clf['svm']=None
            
    def detect(self,x):
        detector1=MatchDetecor(self.clf['match'])
        detector2=SVMDetecor(self.clf['svm'])
        res1=0;res2=0
        if x.has_key('match'):
            res1=detector1.detect(x['match'])
        if x.has_key('svm'):
            res2=detector2.detect(x['svm'])
        else:
            res2=detector2.detect(x['default'])
        res=res1 if res1>0 else res2
        return res

class SVM_RF(Detector):
    def __init__(self, clf=None):
        self.clf=clf if clf else {}
        if not self.clf.has_key('randomForest'):
            self.clf['randomForest']=None
        if not self.clf.has_key('svm'):
            self.clf['svm']=None
    
    def detect(self,x):
        dect1=SVMDetecor(self.clf['svm'])
        dect2=RFDetecor(self.clf['randomForest'])
        try:
            res1=dect1.detect(x['svm'] if x.has_key('svm') else x['default'])
            res2=dect2.detect(x['randomForest'] if x.has_key('randomForest') else x['default'])
            return max(res1,res2)
        except Exception:
            return None
    
def DetectorFactory(method,clf=None):
    if method=='match':
        return MatchDetecor(clf)
    elif method=='svm':
        return SVMDetecor(clf)
    elif method=='match+svm':
        return Match_SVM(clf)
    elif method=='randomForest':
        return RFDetecor(clf)
    elif method=='svm+randomForest':
        return SVM_RF(clf)
    else:
        return None
    
class DetectorBriedge:
    def __init__(self,methods,clfList={}):
        self.methodList=methods
        self.clfSet=clfList
        for m in methods:
            if not clfList.has_key(m):
                self.clfSet[m]=None
        
    def run(self,data):
        detecList=[];res=[]
        for m in self.methodList:
            detecList.append(DetectorFactory(m, self.clfSet[m]))
        for i in len(self.methodList):
            name=Config.Method2Feature[self.methodList[i]]
            if data.has_key(name):
                res.append(detecList[i].detect(data[name]))
            else:
                res.append(detecList[i].detect(data['default']))
        return max(res)
        
        
        

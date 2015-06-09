#coding=utf-8
import os,sys
sys.path.append('.')
from handle.schema import Exp
from handle.extractor import Extractor
from handle.generator import Generator
from lib.androguard.elsim.elsim.elsign import dalvik_elsign 
from lib.androguard.androguard.core.bytecodes import apk
from lib.androguard.androguard.core import androconf
from sklearn import svm
import pickle as pk
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from support.help import (Config,isAPK)

MAXLEN=Exp.objects.count()



def initDB(src,category,start=0,end=MAXLEN):
    
    apkList=[]
    if os.path.isdir(src):
        for item in os.listdir(src):
            tmp=os.path.join(src,item)
#             if isAPK(tmp):
#                 apkList.append(tmp)
#             else:
#                 os.remove(tmp)
            apkList.append(tmp)
    else:
        if isAPK(src):
            apkList.append(src)
    
        else:
            os.remove(src)
            print("Not an APK file")
    start=max(0,start);end=min(end,len(apkList))        
    for apk in apkList[start:end]:
        if Exp.objects(path=apk).count()>0:
            continue
        try:
            row=Exp(path=apk)
            ex=Extractor(apk)
            ge=Generator()
            row.label=category
            row.feature=ge.generateFeature(ex.extractAddition())
            row.save()
            del row,ex
        except:
            continue
        print(apk+" import completed")
        
def randomDB(ratio,start=0,end=MAXLEN):
    for item in Exp.objects[start:end]:
        tmp=np.random.ranf()
        if tmp<ratio:
            item.train=False
        else:
            item.train=True
        item.save()
    

def splitDB(start,end):
    total=Exp.objects.count()
    start=int(max(0.0,start)*total)
    end=int(min(1.0,end)*total)
    for i in range(start):
        Exp.objects[i].update(set__train=True)
    for i in range(start,end):
        Exp.objects[i].update(set__train=False)
    for i in range(end,total):
        Exp.objects[i].update(set__train=True)    
        
    
    

class MyData:
    def __init__(self,isTrain):
        self.isTrain=isTrain  
    def format(self):
        MyData.X=[];MyData.Y=[]
        for item in Exp.objects(train=self.isTrain):
            MyData.X.append(item.feature)
            MyData.Y.append(1 if item.label>0 else 0)
#         MyData.feature=np.array(MyData.feature)
#         MyData.labels=np.array(MyData.labels)

class MyRun:
    def __init__(self,isTrain=False):
        self.isTrain=isTrain  #指定当前行动是训练还是测试
        self.res=[]           #存储测试结果
        self.clf=None         #存储训练所得的分类器参数
    
    def train(self):
        #训练过程
        pass
    
    def test(self):
        #测试过程
        pass
    
    def run(self):
        #被调用的接口
        if self.isTrain:
            self.train()
        else:
            self.test()
            
                
class MyMatch(MyRun):
    database=Config.SigDatabase
    config=Config.SigConfig
    debug=Config.SigDebug
    
    def __init__(self,isTrain,start=0,end=MAXLEN):
        self.isTrain=False
        self.clf=dalvik_elsign.MSignature(MyMatch.database,MyMatch.config,
                                       MyMatch.debug,ps=dalvik_elsign.PublicSignature)
        self.start=start;self.end=end
        
    def test(self,update=False):
        self.res=[]
        for item in Exp.objects[self.start:self.end].filter(train=False):
            if (not update) and (not item.match==None):
                self.res.append(item.match)
                continue
            try:
                a=apk.APK(item.path)
                label=0
                ret=self.clf.check_apk(a)
                if ret[0]==None:
                    self.res.append(0)
                else:    
                    score=[]
                    for tmp in ret[1]:
                        score.append(tmp[1])
                    sim=min(score)
                    if sim<0.1:
                        label=3
                    elif sim<0.2:
                        label=2
                    else:
                        label=1
                del a,ret
                item.match=label
            except:
                item.match=0
            item.save()
            print item.path+' Mactch done!'
        print("Match Process Done!")
        return
        
        
class MySVM(MyRun):
    def train(self):
        self.clf=svm.SVC()
        self.clf.fit(MyData.X,MyData.Y)
        pk.dump(self.clf,open('./support/cache/svm.pk','w'))
    
    def test(self):
        if not self.clf:
            self.clf=pk.load(open('./support/cache/svm.pk','r'))
        self.res=self.clf.predict(MyData.X)
        
        
class MyRandomForest(MyRun):
    def train(self):
        self.clf=RandomForestClassifier(n_estimators=10)
        self.clf.fit(MyData.X,MyData.Y)
        pk.dump(self.clf,open('./support/cache/randomForest.pk','w'))
    def test(self):
        if not self.clf:
            self.clf=pk.load(open('./support/cache/randomForest.pk','r'))
        self.res=self.clf.predict(MyData.X)        
    

class MatchSVM(MyRun):
    def train(self):
        runner=MySVM(self.isTrain)
        runner.train()
        pk.dump(runner.clf,open('./support/cache/svm.pk','w'))
    
    def test(self):
        runner1=MyMatch(self.isTrain)
        runner1.test()
        runner2=MySVM(self.isTrain)
        runner2.test()
        self.res=[x if x>0 else y for x,y in zip(runner1.res,runner2.res)]
#         self.labels=runner1.labels
        return

class MatchRF(MyRun):
    def train(self):
        runner=MySVM(self.isTrain)
        runner.train()
        pk.dump(runner.clf,open('./support/cache/randomForest.pk','w'))
    
    def test(self):
        runner1=MyMatch(self.isTrain)
        runner1.test()
        runner2=MyRandomForest(self.isTrain)
        runner2.test()
        self.res=[x if x>0 else y for x,y in zip(runner1.res,runner2.res)]
#         self.labels=runner1.labels
        return
    
    
class SVMRF(MyRun):
    def train(self):
        runner1=MySVM(self.isTrain)
        runner2=MyRandomForest(self.isTrain)
        runner1.train()
        runner2.train()
        
    def test(self):
        runner1=MySVM(self.isTrain)
        runner2=MyRandomForest(self.isTrain)
        runner1.test()
        runner2.test()
        self.res=[max(x,y) for x,y in zip(runner1.res,runner2.res)]
        return
    
def factory(method,isTrain):
    if method==None:
        print("Must specific a method you want to use")
        return None
    elif method=='svm':
        return MySVM(isTrain)
    elif method=='match':
        return MyMatch(isTrain)
    elif method=='match+svm':
        return MatchSVM(isTrain)
    elif method=='randomForest':
        return MyRandomForest(isTrain)
    elif method=='svm+randomForest':
        return SVMRF(isTrain)
    elif method=='match+randomForest':
        return MatchRF(isTrain)
    else:
        print("No such method for now!")
        return None  

def display(runner):
    if runner.isTrain:
        return
    MM=MN=NM=NN=0;
    for x,y in zip(runner.res,MyData.Y):
        if x>0 and y>0:
            MM+=1
        elif x>0 and y==0:
            MN+=1
        elif x==0 and y>0:
            NM+=1
        elif x==0 and y==0:
            NN+=1
    total=MM+MN+NM+NN
    print("测试样例数："+str(total))
    print("正确检测出的恶意应用数目："+str(MM)+'，占恶意应用中 '+str(100*float(MM)/(max(MM+NM,1)))+"%")
    print("误判的正常应用数目："+str(MN)+'，占正常应用中 '+str(100*float(MN)/(max(MN+NN,1)))+"%")
    print("未检测出的恶意应用数目："+str(NM)+'，占恶意应用中 '+str(100*float(NM)/(max(MM+NM,1)))+"%")
    print("正确分类出的正常应用数目："+str(NN)+'，占正常应用中 '+str(100*float(NN)/(max(MN+NN,1)))+"%")
 
def task(method,isTrain):
    tmp=MyData(isTrain)
    tmp.format()
    runner=factory(method,isTrain)
    if not runner:
        print("Operation abort!")
        return
    runner.run()
    display(runner)
    return   
    
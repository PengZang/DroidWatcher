#coding=utf-8
from sklearn import svm
from handle.schema import Feature
from sklearn.ensemble import RandomForestClassifier
import pickle as pk
class Trainer:
    def __init__(self,savePath,choice='basic'):
        self.savePath=savePath
        self.choice=choice
        self.feature=[];self.labels=[]
        self.clf=None
        
    def format(self):
        for item in Feature.objects(train=True):
            self.feature.append(item.getVect(self.choice))
            self.labels.append(item.label)
        
    
    def train(self):
        pass
    
    
    def save(self):
        if self.clf:
            pk.dump(self.clf, open(self.savePath,'w'))
        else:
            print('Please train the model before saving!')

class SVMTrainer(Trainer):
    def train(self):
        if len(self.labels)==0:
            self.format()
        self.clf=svm.SVC()
        self.clf.fit(self.feature,self.labels)
        

class RFTrainer(Trainer):
    def train(self,n=10):
        if len(self.labels)==0:
            self.format()
        self.clf=RandomForestClassifier(n_estimators=n)
        self.clf.fit(self.feature,self.labels)
        
def trainerFactory(method,choice,savePath):
    if method=='svm':
        return SVMTrainer(savePath,choice)
    elif method=='randomForest':
        return RFTrainer(savePath,choice)
    else:
        return None
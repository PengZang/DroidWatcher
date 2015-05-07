#coding=utf-8
from support.help import Config

class BasicGenerator:
    def __init__(self,option='basic'):
        self.option=option
        
    def generateFeature(self):
        pass

class Generator(BasicGenerator):
    #特征提取的操作
        
    def generatePermission(self,data):
        if not data.has_key('permissionList'):
            print('Please supply Extract result!')
            return None
        permissionList=data['permissionList']
        path=[x['name'] for x in permissionList]
        tmp=Config.permission
        res=[0]*len(tmp)
        for item in path:
            if item in tmp:
                res[tmp.index(item)]=1
        return res

    def generateAPI(self,data):
        if not data.has_key('apiList'):
            print('Please supply Extract result!')
            return None
        constant=['sms','telephony','net','camera','graphics','bluetooth','location']
        res=[0]*len(constant)
        for item in data['apiList']:
            for i in range(len(constant)):
                if constant[i] in item.lower():
                    res[i]=1
        return res
            
            


#     def generateCFG(self):
#         d=self.dex;x=self.vmx;res=''
#         for method in d.get_methods():
#             g = x.get_method(method)
#             if method.get_code() == None:
#               continue
#             res+=method.get_class_name()+method.get_name()+method.get_descriptor()
#             idx = 0
#             for i in g.get_basic_blocks().get():
#                 res+="\t %s %x %x" % (i.name, i.start, i.end)
#                 res+='[ NEXT = ', ', '.join( "%x-%x-%s" % (j[0], j[1], j[2].get_name()) for j in i.get_next() ), ']', '[ PREV = ', ', '.join( j[2].get_name() for j in i.get_prev() ), ']'
#                 for ins in i.get_instructions():
#                     res+="\t\t %x" % idx, ins.get_name(), ins.get_output()
#                     idx += ins.get_length()
#                 res+= ""
#         return res

    def generateFeature(self,data):
        if not data:
            print("Please extract first")
            return None
        tmp=self.generatePermission(data)
        tmp+=self.generateAPI(data)
        return tmp
    
    
def generatorFactory(name):
    if name=='basic':
        return Generator()
    else:
        return None
    
class GeneratorBriedge:
    def __init__(self,featureList=['basic'],data=None):
        self.data=data
        self.featureList=featureList
        
    def generateAll(self):
        res={}
        for f in self.featureList:
            tmp=generatorFactory(f)
            res[f]=tmp.generateFeature(self.data)
        return res
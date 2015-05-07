#coding=utf-8
import sys,os
from optparse import OptionParser
from core import *
from support.help import Config
option_0 = { 'name' : ('-m', '--method'), 'help' : 'Select a method for malware detection', 'nargs' : 1 }
option_1 = { 'name' : ('-i', '--input'), 'help' : 'Directory : scan apk files in this dircetory', 'nargs' : 1 }
option_2 = { 'name' : ('-c', '--category'), 'help' : 'label apks as malware 1 or not malware 0', 'nargs' : 1 }
option_3 = { 'name' : ('-o', '--output'), 'help' : 'Path to store the trained model', 'nargs' : 1 }
options=[option_0,option_1,option_2,option_3]


def main(options,arguments):
    if len(arguments)==0:
        print('Please select your operation to do!')
    elif arguments[0]=='train':
        if options.method==None:
            options.method='svm'
        train(options.method,options.output,Config.FEATURE)
    elif arguments[0]=='init':
        if not options.input:
            print('Must specific file path!')
            return
        if not options.category:
            print('Must specific correct category of apks!')
            return
        options.category=int(options.category)
        options.category=1 if options.category>0 else 0
        initDB(options.input, options.category)
        
    
            
        
        

if __name__=='__main__':
    parser=OptionParser()
    for option in options:
        param = option['name']
        del option['name']
        parser.add_option(*param, **option)

    options,arguments=parser.parse_args()
    sys.argv[:]=arguments
    main(options, arguments)

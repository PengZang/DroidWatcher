#coding=utf-8
import sys,os
from optparse import OptionParser
from core import *
option_0 = { 'name' : ('-m', '--method'), 'help' : 'Select a method for malware detection', 'nargs' : 1 }
option_1 = { 'name' : ('-i', '--input'), 'help' : 'Directory : scan apk files in this dircetory', 'nargs' : 1 }
option_2 = { 'name' : ('-c', '--category'), 'help' : 'label apks as malware 1 or not malware 0', 'nargs' : 1 }
option_3 = { 'name' : ('-s', '--start'), 'help' : 'start position', 'nargs' : 1 }
option_4 = { 'name' : ('-e', '--end'), 'help' : 'end position', 'nargs' : 1 }
options=[option_0,option_1,option_2,option_3,option_4]


def main(options,arguments):
    if not options.input==None:
        options.input=os.path.abspath(options.input)
        if options.category==None:
            print("Must specific the category of apks, malware or not malwre?")
            return
        else:
            options.category=options.category
            start=int(options.start) if options.start else 0
            end=int(options.end) if options.start else 10000
            initDB(options.input, options.category,start,end)
            return
    elif len(arguments)==0:
        print("Must specific the operation you want to do, Train or Test?")
        return
    if arguments[0]=='train':
        isTrain=True
    elif arguments[0]=='test':
        isTrain=False
    else:
        print(" Operation must be train or test")
        return
    task(options.method, isTrain)
    print("All Done!")
            
        
        

if __name__=='__main__':
    parser=OptionParser()
    for option in options:
        param = option['name']
        del option['name']
        parser.add_option(*param, **option)

    options,arguments=parser.parse_args()
    sys.argv[:]=arguments
    main(options, arguments)

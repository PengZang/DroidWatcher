import sys, os
from optparse import OptionParser

option_0 = { 'name' : ('-s', '--standard'), 'help' : '','nargs' : 1 }
option_1 = { 'name' : ('-i', '--input'), 'help' : '', 'nargs' : 1 }
option_2 = { 'name' : ('-o', '--output'), 'help' : '', 'nargs' : 1 }
options = [option_0, option_1, option_2]

def main(options, arguments):
    if not (options.input and options.output and options.standard):
        print("Please first specific arguments")
    if not (os.path.isdir(options.input) and os.path.isdir(options.output) and os.path.exists(options.standard)):
        print("Use illegal options ")
    sta=open(options.standard,'r')
    for item in os.listdir(options.input):
        current = os.path.join(options.input, item)
        if os.path.isdir(current):
            continue
        if item.split('.')[-1]!='yml':
            return
        with open(current,'r') as src,open(os.path.join(options.output,item),'w') as dst:
            tmp=[];count=0
            tmp.append(src.readline())
            tmp.append(sta.readline())
            while tmp[0]:
                if 'bndbox' in tmp[0]:
                    if count>0:
                        break;
                    axis=tmp[1].split(',')
                    string="    - bndbox: {xmin: "+"'"+axis[0]+"', ymin: '"+axis[1]+"', xmax: '"+axis[2]+"', ymax: '"+axis[3]+"'}\r"
                    dst.write(string)
                    count+=1
                else:
                    dst.write(tmp[0])
                tmp[0]=src.readline()
                
            
            
                
if __name__=='__main__':
    parser=OptionParser()
    for option in options:
        param = option['name']
        del option['name']
        parser.add_option(*param, **option)

    options,arguments=parser.parse_args()
    sys.argv[:]=arguments
    main(options, arguments)
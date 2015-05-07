import sys,os
sys.path.append('.')
from lib.androguard.androguard.core import androconf

def isAPK(path):
    ret_type=androconf.is_android(path)
    return (ret_type=='APK')

def main(src):
    if not os.path.isdir(src):
        if not isAPK(src):
            os.remove(src)
        return
    for item in os.listdir(src):
        tmp=os.path.join(src,item)
        if os.path.isdir(tmp):
            main(tmp)
        else:
            if not isAPK(tmp):
                os.remove(tmp)
    return

if __name__ == '__main__':
    src=sys.argv[1]
    main(src)
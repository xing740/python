import os
import sys

sshKey = 'xing@10.17.172.222'

def getDesBaseRout(file):
    return '/data/lsfz_test_s001a/server/' + file + '/svr_source/'

def getVersion():
    return os.getcwd().split("\\").pop()
#---------------------------------------------------
print(sys.argv)

if not len(sys.argv) == 3:
    print("argv error!")
    sys.exit(0)

rout = sys.argv[1]
fileRout = sys.argv[2]

v = rout.split("\\").pop()
fileSplit = fileRout.split('\\')
des = getDesBaseRout(v) + '/' + fileSplit[len(fileSplit) - 2] + '/' + fileSplit.pop()
print(des)
os.system('scp %s %s:%s' % (fileRout, sshKey, des))

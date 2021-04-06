import os
import sys

sshKey = 'xing@10.17.172.222'

def getDesBaseRout(file):
    return '/data/lsfz_test_s001a/server/' + file + '/svr_source/'

def getCopyFile():
    stat = os.popen('svn stat')
    fileVec = stat.read().split()
    finalVec = []
    for it in fileVec:
        if it.endswith('.cpp') or it.endswith('.cpp.h') or it.endswith('h'): 
            finalVec.append(it)
    return finalVec

def getVersion():
    return os.getcwd().split("\\").pop()

def getFileDir(file):
    return file.split("\\")[0]
def doScp(file):
    v = getVersion()
    des = getDesBaseRout(v) + getFileDir(file)
    os.system('scp ./%s %s:%s' %(file, sshKey, des)) 

#---------------------------------------------------
if not len(sys.argv) == 2:
    print("argv error!")
    sys.exit(0)

rout = sys.argv[1]
print("work dir " + rout)

for it in getCopyFile():
    doScp(it)

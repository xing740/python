import os
import sys

sshKey = 'xing@10.20.202.226'
work_pwd = 'F:\cloud\code\zzc'
remote_pwd = '/data/jjdzc_test_s001a/server/'

def getCopyFile():
    stat = os.popen('svn stat')
    fileVec = stat.read().split()
    finalVec = []
    for it in fileVec:
        if it.endswith('.ts'):
            finalVec.append(it)
    return finalVec

def doScp(file):
    des_pwd = remote_pwd + file;
    print(des_pwd)
    os.system('scp ./%s %s:%s' %(file, sshKey, des_pwd)) 

#---------------------------------------------------
os.chdir(work_pwd)
print(os.getcwd())

for it in getCopyFile():
    doScp(it)

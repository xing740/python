import os
import sys

sshKey = 'xing@10.20.202.226'
work_pwd = 'f:\cloud\code\zzc\\'
remote_pwd = '/data/jjdzc_test_s001a/server/'

#---------------------------------------------------
file = sys.argv[1]
des_pwd = file.replace(work_pwd, remote_pwd)
os.system('scp %s %s:%s' %(file, sshKey, des_pwd)) 

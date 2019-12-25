#!/user/bin/env python
#coding:utf-8

import os
import sys
import subprocess
import json

def getPid(na): #-v是屏蔽某字段
    outPut = subprocess.Popen('ps aux | grep %s |grep -v grep' % (na),stdout=subprocess.PIPE,shell=True).communicate()
    l = outPut[0].split()
    if len(l) == 0: return
    else: return l[1]

def getMongoInfo():
    outPut = subprocess.Popen('find -name game_cfg.json |grep -v bin',stdout=subprocess.PIPE,shell=True).communicate()
    with open('%s' % (outPut[0].strip('\n')), 'r') as fp:
        data = json.load(fp)
        return data['mongodb']

def useLinusPs(sid):
    outPut = subprocess.Popen('ps aux | grep %s' % (sid),stdout=subprocess.PIPE,shell=True).communicate()
    print outPut[0]

#分离出操作符和服务器
def getOpAndSid():
    arg = sys.argv[1]
    op = ""
    sid = ""
    for a in arg:
        if a.isdigit(): sid += a
        else: op += a
    print "op:" + op + " sid: " + sid
    return op, sid

def debug():#gdb ./gg corefile
    outPut = subprocess.Popen('ls -l',stdout=subprocess.PIPE,shell=True).communicate()
    l = outPut[0].split()
    for str in l:
        if str.find('core.') == -1: continue
        else: os.system('gdb ./gg %s' % str)
        break

routeMap = {
        '001': 'lsfz_test_s001a',
        '017': 'fytx2_test_p017a',
        '003': 'lsfz_test_s003a',
        '004': 'lsfz_test_s004a',
        '3003': 'fytx2_test_p3003a',
        '3004': 'fytx2_test_p3004a',
        '3005': 'fytx2_test_p3005a',
        '3006': 'fytx2_test_p3006a',
        '3007': 'fytx2_test_p3007a',
        '3008': 'fytx2_test_p3008a',
        '4003': 'fytx2_test_p4003a',
        '4004': 'fytx2_test_p4004a',
        '4005': 'fytx2_test_p4005a',
        '4006': 'fytx2_test_p4006a',
        }


op, sid = getOpAndSid()

sRoute = '/data/' + routeMap[sid] + '/server' #server dir
print 'sRoute:' + sRoute
gRoute = sRoute + '/svr_source/game'   #game dir

#取出gg 和 gg screen 的 pid
scrnNa = routeMap[sid] + '_gg'
ggNa = routeMap[sid] + '/server/gg'

scrnPid = getPid(scrnNa)


#改变工作目录  默认server目录
os.chdir(sRoute)
os.system('pwd')

#执行
if op == 's': #screen -r pid
    pid = getPid(scrnNa)
    print "screen pid:" + pid
    os.system('screen -r %s' % (pid))
elif op == 'gdb': #gdb attach pid
    os.system('./start.sh')
    pid = getPid(ggNa)
    print "gg pid:" + pid
    os.system('gdb attach %s' % (pid))
elif op == 'ls':#server dir
    os.system('ls -l')
elif op == "mg":
    mgInfo = getMongoInfo()
    print "mgInfo:" + mgInfo
    os.system('mongo %s' % (mgInfo))
elif op == "ps":
    useLinusPs(sid)
elif op == "debug":
    debug()
elif op == "stat":
    os.system('stat gg')
else:
    print "op:" + op + " is not exists!"



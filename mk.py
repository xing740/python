#!/usr/bin/python
#coding:utf-8

import os
import sys

def printInfo(r, fc, fo):
    os.system('echo  -std=gnu++14 -c %s/%s -o obj/game/%s -I/usf/local/include -I/usr/local/include/mongo -I. -I../common -I../net -I../game_def/ -O0 -g3 -Wreturn-type -Wno-pragmas -gdwarf-2' % (r, fc, fo))

def doMake(fc, fo):
    fp = os.popen('pwd')
    route = fp.read().strip('\n')
    printInfo(route, fc, fo)
    return os.system('g++ -std=gnu++14 -c %s/%s -o obj/game/%s -I/usr/local/include -I/usr/local/include/mongo -I. -I../common -I../net -I../game_def/ -O0 -g3 -Wreturn-type -Wno-pragmas -gdwarf-2' % (route, fc, fo))

def getCppAndOFileName(na):
    return na + '.o'

print sys.argv

if len(sys.argv) == 2 or len(sys.argv) == 1: 
    stat = os.popen('svn stat')
    vec = stat.read().split()
    #print vec
    arg1 = ""
    if len(sys.argv) == 2:
        arg1 = sys.argv[1]
    for f in vec:
        if arg1 != "" and f.find(arg1) < 0:
            continue
        arg1 = ""
        if f.endswith('.cpp') or f.endswith('.cpp.h'):
            fcpp = f
            fo = getCppAndOFileName(f.replace(".cpp","").replace(".h", ""))
            ret = doMake(fcpp, fo)
            if ret != 0: break
else:
    print "arg worry!"
                

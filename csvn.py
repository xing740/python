#!/usr/bin/python
#coding:utf-8

import os
import sys
note = sys.argv[1] #注释

r = os.popen('svn stat')
info = r.readlines()
allFile = ''
for l in info:
    l = l.strip('\n').split('       ')
    stat = l[0]
    fileName = l[1]
    #print "stat:" + stat + " fn:" + fileName
    if (stat != 'M') or (fileName == 'task_checker.h'):
        continue
    allFile += " "
    allFile += fileName

print "allFile: " + allFile

if allFile != '':
    os.system("svn commit -m %s %s" % (note, allFile))



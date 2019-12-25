#!/usr/bin/python
#coding:utf-8

import os
import sys

if len(sys.argv) != 2:
    print "arg worry!"
    sys.exit(0)

arg = sys.argv[1]

trash = '/home/xing/.trash'
if arg == 'clean':
    os.chdir(trash)
    os.system('rm -rf *')
elif arg == 'ls':
    os.chdir(trash)
    os.system('ls -l')
else:
    os.system('mv ./%s %s' % (arg, trash))



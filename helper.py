#!/user/bin/env python
#coding:utf-8

import os
import sys
import subprocess
import json
import yaml
import pymongo

class Help(object):
    def __init__(self, op, sid, args):
        args = sys.argv[1].split(':')

        self._op = op
        self._server_id = sid
        self._args = args
        self._do_map = {
                's': self.doScreen,
                'gdb': self.doAttachGG,
                'ps': self.doProgressInfo,
                'ssh': self.doSSH,
                'sync': self.doSyncFile,
                'mg':self.doOpenMongo,
                'ls':self.doServerDirInfo,
                'dmg':self.doDownloadMongo,
                'rmg':self.doRestoreMongo,
                'cmg':self.doCleanMongo,
                'change':self.doChangeVersion,
                }
        self._ssh_addr_map = {
                "3003":'10.20.202.218',
                "3004":'10.20.202.218',
                "3005":'10.20.202.218',
                "3006":'10.20.202.218',
                "3007":'10.20.202.218',
                "3008":'10.20.202.218',
                "20001":'10.21.210.210',
                "20002":'10.21.210.210',
                "20003":'10.21.210.210'
                }
        self._server_dir_map = {
                '55': 'lsfz_test_s001a',
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
                '002': 'lsfz_test_s002a',
                '019': 'fytx2_test_p019a',
                '003': 'lsfz_world_s003',
                "20001":'jshp_test_s20001a',
                "20002":'jshp_test_s20002a',
                "20003":'jshp_test_s20003a'
                }

    #-v是屏蔽某字段
    def getPid(self, name):
        outPut = subprocess.Popen('ps aux | grep %s |grep -v grep' % (name),stdout=subprocess.PIPE,shell=True).communicate()
        return outPut[0].split()[1]

    def goServerDir(self):
        addr = os.path.join('/data', self._server_dir_map[self._server_id], 'server')
        os.chdir(addr)

    def doProgressInfo(self):
        outPut = subprocess.Popen('ps aux | grep %s' % (self._server_id),stdout=subprocess.PIPE,shell=True).communicate()
        print outPut[0]

    def noNeedIndentMongo(self):
        sid = ['55', '3000', '001']
        if self._server_id in sid:
            return True;
        else:
            return False;

    def doCleanMongo(self):
        self.goServerDir()
        file_addr = os.path.join('.', 'server', 'game_cfg.json')
        with open('%s' % (file_addr), 'r') as fp:
            data = json.load(fp)

        cfg = yaml.load(file('../optconfig.yaml'))
        server_id = cfg['GAME_CONFIG']['SERVER_ID']

        conn = pymongo.MongoClient(data['mongodb'])
        conn.drop_database('sid%s' %(server_id))
        if server_id not in conn.database_names():
			sys.stdout.write('clean mongodb success!\n')
        else:
			sys.stdout.write('clean mongodb fail!\n')

    def doRestoreMongo(self):
        self.doCleanMongo()

        dir_addr = self._args[2]
        if self.noNeedIndentMongo():
            os.system('mongorestore -h 10.17.172.222:37017 -d sid%s %s' %(self._server_id, dir_addr))
        else:
            port, user, passwd, server_id = self.mongoIdentInfo()
            os.system('mongorestore --port %s -u %s -p %s --authenticationDatabase=admin --authenticationMechanism=MONGODB-CR -d sid%s %s' % (port, user, passwd, server_id, dir_addr))

    def doDownloadMongo(self):
        if self.noNeedIndentMongo():
            os.system('mongodump -h 10.17.172.222:37017 -d sid%s -o ./' %(self._server_id))
        else:
            os.system('mongodump --port %s -u %s -p %s --authenticationDatabase=admin --authenticationMechanism=MONGODB-CR -d sid%s -o ./' % (self.mongoIdentInfo()))

    def mongoIdentInfo(self):
        self.goServerDir()
        cfg = yaml.load(file('../optconfig.yaml'))
        return cfg['GAME_CONFIG']['MONGODB_PORT'], cfg['GAME_CONFIG']['MONGODB_USER'], cfg['GAME_CONFIG']['MONGODB_PASS'], cfg['GAME_CONFIG']['SERVER_ID']

    def doServerDirInfo(self):
        self.goServerDir()
        os.system('ls -1')

    def doOpenMongo(self):
        self.goServerDir()
        file_addr = os.path.join('.', 'server', 'game_cfg.json')
        with open('%s' % (file_addr), 'r') as fp:
            data = json.load(fp)
        os.system('mongo %s' %(data['mongodb']))

    def doSyncFile(self):
        s = set()
        for k, v in self._ssh_addr_map.items():
            s.add(v)
        while len(s) > 0:
            addr = s.pop()
            os.system("scp /home/xing/xpython/helper.py root@%s:/bin/" % addr)
            os.system("scp /home/xing/xbin/other_uh root@%s:/bin/uh" % addr)
            print addr

    def doSSH(self):
        os.system('ssh root@%s' % (self._ssh_addr_map[self._server_id]))

    def doScreen(self):
        pid_name = self._server_dir_map[self._server_id] + '_gg'
        os.system('screen -r %s' %(self.getPid(pid_name)))

    def doAttachGG(self):
        self.goServerDir()
        pid_name = self._server_dir_map[self._server_id] + '/server/gg'
        os.system('gdb attach %s' %(self.getPid(pid_name)))

    def doChangeVersion(self):
        name = self._args[1]
        baseRout = '/data/lsfz_test_s001a/server/'
        name_rout = baseRout + name
        if os.path.exists(name_rout) == False:
            print "no exists: " + name 
            return

        os.chdir(baseRout)
        os.system('rm -rf svr_source')
        os.system('rm -rf gg')
        os.system('rm -rf as')

        os.system('ln -s ./%s/svr_source ./' %name)
        os.system('ln -s ./%s/svr_source/game/gg ./' %name)
        os.system('ln -s ./%s/svr_source/activity_server/as ./' %name)
        print 'change to ' + name + " success!"

    def do(self):
        do_func = self._do_map.get(self._op)
        if do_func is not None:
            do_func()
        else:
            print "op: " + self._op + ' error!'

if __name__ == '__main__':
    args = sys.argv[1].split(':')
                
    help = Help(args[0], args[1], args)
    help.do()


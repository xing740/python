#!/usr/bin/python3

import os
import xml.dom.minidom
import xml.etree.ElementTree as ET
from datetime import datetime

#包含所有要修改文件的目录地址(绝对或相对)
mainAddr = r"D:\\projects"
#mainAddr = r".\\"

#正常交易WEEK区间 周一到周五
tdWStart = 0
tdWEnd = 4

#正常交易HOUR区间
tdHStart = 8
tdHEnd = 15

#交易ctp 配置目录
tdCfgDir = "tradeapi\CTP_Trade\\" 
#行情ctp 配置目录
mKCfgDir = "marketapi\CTP_Market\\" 

def modifyCTPFrontAddress(path):
	#读取xml文件到内存
	fp = open(path, encoding='gb2312')
	strData = fp.read()
	fp.close()

	#将内存中的数据进行xml解析
	doc = xml.dom.minidom.parseString(strData)

	#取树根
	rootNode = doc.documentElement

	#取要更新的结点
	names = rootNode.getElementsByTagName("FrontAddress")

	#遍历取到的结点进行修改
	for text in names:

		#取当前时间信息
		curTime = datetime.now()
		hour = curTime.hour
		week = curTime.today().weekday()

		#判断是否是交易服
		if path.find(tdCfgDir) > 0:
			#正常交易时间地址
			if tdWStart <= week <= tdWEnd and tdHStart <= hour <= tdHEnd:
				text.childNodes[0].data = "tcp://180.168.146.187:10202"

			#24小时交易地址
			else: 
				text.childNodes[0].data = "tcp://180.168.146.187:10130"
			print("trade: " + text.childNodes[0].data)

		#判断是否是行情服
		elif path.find(mKCfgDir) > 0:
			#正常交易时间地址
			if tdWStart <= week <= tdWEnd and tdHStart <= hour <= tdHEnd:
				text.childNodes[0].data = "tcp://180.168.146.187:10211"

			#24小时交易地址
			else:
				text.childNodes[0].data = "tcp://180.168.146.187:10131"
			print("market: " + text.childNodes[0].data)

	#保存文件
	with open(path, 'w') as f:
		doc.writexml(f, encoding='gb2312')


def getXmlFiles(path):
	allDir=[]
	dir = ""
	# [地址,文件夹名,文件名]
	for dirpath,dirnames,filenames in os.walk(path):
		#遍历文件夹
		for dir in dirnames:
			#组成地址
			dir = os.path.join(dirpath,dir)
			if dir.endswith('.xml'):
				if dir.find(tdCfgDir) > 0 or dir.find(mKCfgDir) > 0:
					allDir.append(dir)
		#遍历文件
		for name in filenames:
			#组成地址
			dir = os.path.join(dirpath, name)
			if dir.endswith('.xml'):
				if dir.find(tdCfgDir) > 0 or dir.find(mKCfgDir) > 0:
					allDir.append(dir)
	return allDir



if __name__ == '__main__':
	#取所有要修改的xml文件
	files=getXmlFiles(mainAddr)

	#遍历修改xml文件
	for f in files:
		print(f)
		#修改 ctp 前置地址
		modifyCTPFrontAddress(f)


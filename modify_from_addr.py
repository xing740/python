#!/usr/bin/python3

import os
import xml.dom.minidom
from datetime import datetime

#取当前时间
dt = datetime.now()

tradeDay = [1,2,3,4,5]

def modifyCTPFrontAddress(path):
	#读取xml文件到内存
	file_object = open(path)
	ori_xml = file_object.read()
	file_object.close()
	#转换数据编码
	pro_xml = ori_xml.replace("utf-8", "gb2312")
	#将内存中的数据进行xml解析
	doc = xml.dom.minidom.parseString(pro_xml)
	#取的树根
	rootNode = doc.documentElement
	#取要更新的结点
	names = rootNode.getElementsByTagName("FrontAddress")
	#遍历取到的结点
	for name in names:
		#修改交易服的 ctp_trade
		if path.find("tradeapi\CTP_Trade") >= 0:
			if dt.hour < 12 and path.find:
				#正常交易时间
				name.childNodes[0].data = "tcp://180.168.146.187:10202"
			else: 
				#24小时交易
				name.childNodes[0].data = "tcp://180.168.146.187:10130"
			print("tradeapi" + " " + path + " " + name.childNodes[0].data)	
		#修改行情服和行情服的的 ctp_market
		elif path.find("marketapi\CTP_Market") >= 0:
			if dt.hour < 12 and path.find:
				#正常交易时间
				name.childNodes[0].data = "tcp://180.168.146.187:10211"
			else:
				#24小时交易
				name.childNodes[0].data = "tcp://180.168.146.187:10131"
			print("markdetapi" + " " + path + " " + name.childNodes[0].data)	

	#保存文件
	with open(path, 'w') as f:
		# 缩进 - 换行 - 编码
		doc.writexml(f, addindent='  ', encoding='gb2312')


def getXmlFiles(path):
	allfile=[]
	dir = ""
	# [地址,文件夹名,文件名]
	for dirpath,dirnames,filenames in os.walk(path):
		#遍历文件夹
		for dir in dirnames:
			#组成地址
			dir = os.path.join(dirpath,dir)
			if dir.endswith('.xml'):
				allfile.append(dir)
		#遍历文件
		for name in filenames:
			#组成地址
			dir = os.path.join(dirpath, name)
			if dir.endswith('.xml'):
				allfile.append(dir)
	return allfile



if __name__ == '__main__':
	#根目录
	path = "./"
	#取所以xml文件
	allfile=getXmlFiles(path)
	#遍历修改xml文件
	for file in allfile:
		#print(file)
		#修改 ctp 柜台
		modifyCTPFrontAddress(file)

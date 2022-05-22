# -*- coding: utf-8 -*-
# !/usr/bin/env python

import os
import shutil


class CopyFile(object):
	def __init__(self):
		#复制力度
		self.copyMarketDebug = False
		self.copyMarketRelease = False
		self.copyTradeDebug = True
		self.copyTradeRelease = False

		#需要的文件路径
		self.srcToDecMap = {
			'./tradeapi/bin/x64/Debug/tradeapid.dll' : 'tradeserver/bin/x64/Debug/tradeapi/tradeapid.dll',
			'./tradeapi/bin/x64/Debug/CTP_Traded.dll' : 'tradeserver/bin/x64/Debug/tradeapi/CTP_Trade/CTP_Traded.dll'
		}

	def doCopy(self, k, v):
		shutil.copy2(k, v)
		print("copy success! " + v)

	def start(self):
		for key, value in self.srcToDecMap.items():
			if key.find("Debug") >= 0:
				if self.copyMarketDebug == True and key.find("market", 0, 10) >= 0:
					self.doCopy(key, value) # 行情服debug
				if self.copyTradeDebug == True and key.find("trade", 0, 10) >= 0:
					self.doCopy(key, value) # 交易服debug

			if key.find("Release") >= 0:
				if self.copyMarketRelease == True and key.find("market", 0, 10) >= 0:
					self.doCopy(key, value) # 行情服release
				if self.copyTradeRelease == True and key.find("trade", 0, 10) >= 0:
					self.doCopy(key, value) # 交易服release

if __name__ == '__main__':
	copyFile = CopyFile()
	copyFile.start()

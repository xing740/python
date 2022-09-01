import contextlib
from json import tool
from sqlite3 import Time
import time

import PIL  # 图像处理库
import pyautogui  # 鼠标 键盘 图像
import pyperclip  # 剪切板

MoveSleepSec = 0.01

"""

图片相关

#不传参数只截图  不保存
img = pyautogui.screenshot()
#某图片参数位置的RPC颜色
print(img.getpixel((100,200)))

#参数位置的RGB颜色
pyautogui.moveTo(2783,341)
print(pyautogui.pixel(2783,341))

判断某位置RGB颜色
pyautogui.pixelMatchesColor(100, 200, (255, 255, 255))



#点击复制
pyautogui.moveTo(2791,635)
#time.sleep(0.5)
pyautogui.click()
#time.sleep(0.5)


"""

class ToolMgr:
	def __init__(self):
		pass #是占位，让代码整体完

	#设置剪切板内容
	@staticmethod  #静态方法
	def SetCopy(param):
		pyperclip.copy(param)

	#获取剪切板内容
	@staticmethod  #静态方法
	def GetPaste():
		return pyperclip.paste()

	@staticmethod  #静态方法
	def Read(x = -1, y = -1):
		ToolMgr.Click(x, y)
		ToolMgr.HoldPress('ctrl',['a', 'c'])
		return ToolMgr.GetPaste()

	#往输入框写入数据
	@staticmethod  #静态方法
	def Writer(str, x = -1, y = -1):
		#写入
		pyautogui.typewrite(str)

	#按下hold键，再按pressArr中的键，最后放开hold键
	#with pyautogui.hold('ctrl'):
		#pyautogui.press(['a','c'])
	@staticmethod  
	def HoldPress(hold, pressArr):
		with pyautogui.hold(hold):
			pyautogui.press(['a','c'], 1, 0.2)

	#获取某坐标的RGB 
	#返回 (x, x, x)
	@staticmethod  
	def GetPosRGB(x = -1, y = -1):
		#没有传参数 默认取当前鼠标坐标
		if x == -1 or y == -1: 
			x, y = pyautogui.position()
		return pyautogui.pixel(x, y)

	#移动到某座标再点击
	@staticmethod  
	def Click(x = -1, y = -1):
		ToolMgr.MoveTo(x, y)
		pyautogui.mouseDown()
		pyautogui.mouseUp()

	#移动点击，判断点击位RGB不同才算点击成功
	@staticmethod  
	def ClickAndRGB(x = -1, y = -1):
		ToolMgr.MoveTo(x, y)
		orx, ory, orz = ToolMgr.GetPosRGB(x, y)
		pyautogui.mouseDown()
		pyautogui.mouseUp()
		crx, cry, crz = ToolMgr.GetPosRGB()
		while True:
			if orx != crx or ory != cry or orz != crz:
				return
			else:
				pyautogui.sleep(0.01)

	@staticmethod  
	def	RGBEqual(x, y, rgbx, rgby, rgbz):
		r, p, g = ToolMgr.GetPosRGB(x, y)
		if r == rgbx and p == rgby and g == rgbz:
			return True
		else:
			return False


	#移动到某坐标
	def MoveTo(x1, y1):
		#判断坐标参数
		if x1 < 0 or y1 < 0:
			return
		#移动
		pyautogui.moveTo(x1, y1)
		#循环判断是否完成移动
		while True: 
			curX, curY = pyautogui.position()
			if x1 == curX and y1 == curY:
				return
			else:
				time.sleep(MoveSleepSec)
	

	"""
	查找屏幕上的所有图片的中心度座标
	addr:图片地址
	confidence:模糊度
	offset:下一匹配的图偏移中心点的像素
	"""
	@staticmethod  
	def GetAllImageCenterPos(addr, confid = 1, offset = 0):
		allPos = []
		images = pyautogui.locateAllOnScreen(addr, confidence = confid)
		lastx = lasty = -1
		for pos in images:
			x, y = pyautogui.center(pos)
			if lastx != -1 and lasty != -1 and offset > 0:
				difx = abs(lastx - x)
				dify = abs(lasty - y)
				if difx <= offset and dify <= offset:
					continue
			#ToolMgr.MoveTo(x, y)
			#pyautogui.sleep(0.5)
			allPos.append((x, y))
			lastx = x
			lasty = y
		return allPos

	#移动到x,y位置,滚动鼠标 step 正 向上滚， 负 向下滚
	@staticmethod  
	def Scroll(step, x = None, y = None):
		if x != None and y != None:
			ToolMgr.MoveTo(x, y)
		pyautogui.scroll(step)
	
	"""
	取以某坐标为中心的延展十字位的rgb
	posx, posy, 位置座标
	num 每一个方向取的点数
	perPoint 每个点偏移的像素位
	# return [{pos:(x, y), rgb:(r, g, b)}, ...]
	"""
	@staticmethod  
	def GetAreaRGB(num, perPoint, posx = -1, posy = -1):
		if posx < 0 or posy < 0: 
			posx, posy = pyautogui.position()
		posArr = []
		for n in range(num):
			x = posx + n * perPoint
			posArr.append({'pos':(x, posy), 'rgb': ToolMgr.GetPosRGB(x, posy)})

			x = posx - n * perPoint
			if x < 0:
				x = 0
			posArr.append({'pos':(x, posy), 'rgb': ToolMgr.GetPosRGB(x, posy)})

			y = posy - n * perPoint
			if y < 0:
				y = 0
			posArr.append({'pos':(posx, y), 'rgb': ToolMgr.GetPosRGB(posx, y)})

			y = posy + n * perPoint
			posArr.append({'pos':(posx, y), 'rgb': ToolMgr.GetPosRGB(posx, y)})
		return posArr
	
	#判断数组中的位置与RGB与当前的位置RGB是否一至
	# arr [{pos:(x, y), rgb:(r, g, b)}, ...]
	@staticmethod  
	def CheckAreaRGB(arr):
		for it in arr:
			rgb = ToolMgr.GetPosRGB(it['pos'][0], it['pos'][1])
			if rgb != it['rgb']:
				return False
		return True

	




#pyautogui.scroll(100)
#pyautogui.scroll(-1100, x= 12, y = 1)
#ToolMgr.Scroll(-1100, 931, 521)
"""
ToolMgr.MoveTo(100, 100)
a = ToolMgr.AreaRGB(100, 100, 10, 2)
time.sleep(3)
print(ToolMgr.CheckAreaRGB(a))
"""

while True:
	posRgbArr = ToolMgr.GetAreaRGB(10, 10)
	ToolMgr.Scroll(-500)
	pyautogui.sleep(0.2)
	if ToolMgr.CheckAreaRGB(posRgbArr):
		while True:
			posRgbArr = ToolMgr.GetAreaRGB(10, 10)
			pyautogui.sleep(0.2)
			ToolMgr.Scroll(10000)
			if ToolMgr.CheckAreaRGB(posRgbArr):
				break

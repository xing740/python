import time
import PIL  #图像处理库
import pyautogui  #鼠标 键盘 图像
import pyperclip  #剪切板


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
	def Copy(param):
		pyperclip.copy(param)

	#获取剪切板内容
	@staticmethod  #静态方法
	def GetPaste():
		return pyperclip.paste()

	@staticmethod  #静态方法
	def Writer(str):
		pyautogui.typewrite(str)

	#按下hold键，再按pressArr中的键，最后放开hold键
	#with pyautogui.hold('ctrl'):
		#pyautogui.press(['a','c'])
	@staticmethod  
	def HoldPress(hold, pressArr):
		with pyautogui.hold(hold):
			pyautogui.press(pressArr)

	#获取某坐标的RGB 
	#返回 (x, x, x)
	@staticmethod  
	def GetPosRGB(x=0, y=0):
		#没有传参数 默认取当前鼠标坐标
		if x == y == 0: 
			x, y = pyautogui.position()
		return pyautogui.pixel(x, y)

	#移动到某坐标点击
	@staticmethod  
	def Click(x = 0, y = 0):
		pyautogui.moveTo(x, y)
		while True:
			curX, curY = pyautogui.position()
			if x == curX and y == curY:
				pyautogui.click()
				return
			else:
				time.sleep(MoveSleepSec)

	#移动到某坐标
	def MoveTo(x, y):
		pyautogui.moveTo(x, y)
		#循环判断是否完成移动
		while True: 
			curX, curY = pyautogui.position()
			if x == curX and y == curY:
				return
			else:
				time.sleep(MoveSleepSec)




	
import time
from threading import Timer
import pyautogui

def doTick():
	Timer(30 * 60, doTick).start()
	tm = time.asctime(time.localtime(time.time()))
	pyautogui.alert(text=tm, title="", button="OK")

if __name__ == '__main__':
	min = time.localtime(time.time()).tm_min
	interval = 60 - min if min > 30 else 30 - min
	Timer(interval * 60, doTick).start();
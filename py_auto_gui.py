import pyautogui
import time
#print(pyautogui.size())
#print(pyautogui.position())

pyautogui.FAILSAFE = False

pos = pyautogui.position()
pyautogui.screenshot(r"F:\git_code\python\2.png", region=(pos.x, pos.y, 72, 98))
time.sleep(3)
im = pyautogui.locateOnScreen(r"F:\git_code\python\2.png");
print(im)





#pyautogui.moveTo(100, 100)
#pyautogui.moveTo(0, 0)
#pyautogui.moveTo(im.left, im.top, duration=3)
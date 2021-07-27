import json
import os
import random
import sys
import time
import tkinter
from multiprocessing import Process
import psutil
import pyautogui as ai
from pynput.keyboard import Listener
from PIL import Image
import pytesseract
import pyperclip

#print(pyautogui.size())
#print(pyautogui.position())

ai.FAILSAFE = False

#pos = ai.position()
#print(pos)
#ai.screenshot(r"F:\git_code\python\2.png", region=(pos.x, pos.y, 30, 30))
#time.sleep(3)
#im = ai.locateOnScreen(r"F:\git_code\python\2.png")
#print(im)
#ai.moveTo(im.left, im.top)
for p in ai.locateAllOnScreen(r"F:\git_code\python\2.png"):
    time.sleep(1)
    ai.moveTo(p.left, p.top)
    time.sleep(1)
    ai.screenshot(r"F:\git_code\python\3.png", region=(p.left, p.top, 398, 40))
    im = Image.open('3.png')
    text = pytesseract.image_to_string(im, lang='chi_sim')
    print(text)
    x = text
    pyperclip.copy(x)
    time.sleep(1)
    #打开
    ai.click(button="right")
    ai.moveRel(5, 30)
    time.sleep(1)
    ai.click()
    #保存
    time.sleep(3)
    ai.click(button="right")
    ai.moveRel(5, 96)
    time.sleep(1)
    ai.click()
    #改名
    time.sleep(3)
    ai.hotkey("ctrl", "v")
    #点击保存
    m = ai.locateOnScreen(r"F:\git_code\python\save.png")
    cm = ai.center(m)
    ai.click(cm.x, cm.y)
    #关浏览器
    ai.hotkey("ctrl", "w")

    sys.exit()

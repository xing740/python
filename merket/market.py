import json
import multiprocessing
import os
import random
import string
import sys
import time
import tkinter
from json import tool
from multiprocessing import Process
from sqlite3 import Time

import psutil
import pyautogui as ai
from numpy import diff
from PIL import Image
from pynput.keyboard import Listener

from market_test import *

#正在挂单买的像素点的RGB
OnBuyRGB = (183, 154, 127)


item_id_interval = 1000
wu_qi = 1
zhuan_bei = 2
fu_shou = 3
other = 4
empty_id = 5
error_id = 6
itemDir = "items"
tmp_item_name = "9999.png"
empty_name = "10000.png"
valMap = {}
ids = []

def delSame(path, id):
    image1 = Image.open(path)
    image1 = make_regalur_image(image1)
    name1 = str(id) + ".png"
    for it in ids:
        if it == name1:
            continue
        image2 = valMap.get(it)
        if image2 == None:
            continue
        val = calc_similar(image1, image2)
        if val >= 0.7:
            if os.path.exists("%s\%s" %(itemDir, it)):
                os.remove("%s\%s" %(itemDir, it))

def CalSameVal():
    image1 = Image.open("%s\%s" %(itemDir, tmp_item_name))
    image1 = make_regalur_image(image1)
    for it in ids:
        if it == tmp_item_name:
            continue
        #image2 = Image.open("%s\%s" %(itemDir, it))
        #image2 = make_regalur_image(image2)
        image2 = valMap.get(it)
        if image2 == None:
            continue
        val = calc_similar(image1, image2)
        if val >= 0.66:
            print("val:"+str(val)+" itemId:"+str(it))
            return int(it[0]) if it != empty_name else empty_id
    return error_id
def wear():
    changeBox(other)
    ai.click(113,204)
    time.sleep(0.5)
    ai.click(113,341)
    time.sleep(0.5)
    ai.click(291,200)

def changeBox(itemType):
    ai.click(151, 271) #点击装备库
    time.sleep(0.5)
    if itemType == wu_qi:
        ai.click(143, 350)
    elif itemType == zhuan_bei:
        ai.click(143, 325)
    elif itemType == fu_shou:
        ai.click(143, 300)
    else: #首页
        ai.click(143, 407)

def JudgeType():
    x = 1560
    y = 524
    ix = 55
    iy = 49
    t = 82
    old_type = 0
    item_type = other

    #点击堆叠
    ai.click(1765,969)

    while True:
        type_info_arr = [] #[type,posx,poxy]

        #点击整理
        ai.click(1838, 970)

        ticks = time.time()
        time.sleep(0.5)
        for i in range(5):
            if item_type == 444: #空白框
                break
            for j in range(4):
                posx = x + j * t
                posy = y + i * t
                ai.screenshot("%s\%s" %(itemDir, tmp_item_name), region=(posx, posy, ix, iy))
                item_type = CalSameVal()
                if item_type == error_id:
                    item_type = other
                type_info_arr.append(item_type)#图片类型

                #图片坐标 
                type_info_arr.append(posx)
                type_info_arr.append(posy)

                if item_type == empty_id:
                    item_type == 444
                    break

        print("use time: " + str(time.time() - ticks))
        print(type_info_arr)

        ai.keyDown("shift")
        i = 0
        while i < len(type_info_arr):
            txy = type_info_arr[i]
            i+=1
            px = type_info_arr[i]
            i+=1
            py = type_info_arr[i]
            i+=1

            print("type:"+str(txy))
            if txy == empty_id:
                ai.keyUp("shift")
                return

            if txy != old_type:
                changeBox(txy)
                old_type = txy

            ai.moveTo(px + ix / 2, py + iy / 2)
            print("type:"+str(txy))
            print("x:"+str(px))
            print("y:"+str(py))
            ai.mouseDown()
            ai.mouseUp()
            ai.mouseDown()
            ai.mouseUp()

def initMap():
    valMap.clear()
    ids.clear()
    tmp = os.listdir(itemDir)
    for it in tmp:
        ids.append(it)
        if it == tmp_item_name:
            continue
        if os.path.exists("%s\%s" %(itemDir, it)) == False:
            continue
        image2 = Image.open("%s\%s" %(itemDir, it))
        valMap[it] = make_regalur_image(image2)
    #print(valMap)

def randomFloat(num, half=0):
    if half == 0:
        half = num / 2
    return random.uniform(num - half, num + half)

# 将图片转化为RGB
def make_regalur_image(img, size=(64, 64)):
    gray_image = img.resize(size).convert('RGB')
    return gray_image
 
# 计算直方图
def hist_similar(lh, rh):
    assert len(lh) == len(rh)
    hist = sum(1 - (0 if l == r else float(abs(l-r))/max(l,r))for l, r in zip(lh, rh))/len(lh)
    return hist
 
# 计算相似度
def calc_similar(li, ri):
    calc_sim = hist_similar(li.histogram(), ri.histogram())
    return calc_sim

def randomInt(num, half=0):
    if half == 0:
        half = num / 2
    left = num - half if num - half > 1 else 1
    return random.randint(int(left), int(num + half))


def clickImage(args, pos):
    x = args.left
    y = args.top
    if pos == "centre":
        x += args.width / 2
        y += args.height / 2
    elif pos == "leftDown":
        y += args.height
    elif pos == "rightUp":
        x += args.width
    elif pos == "rightDown":
        x += args.width
        y += args.height
    ai.click(x, y)


def judgeImageExists(image):
    i = 0
    ok = "再找一次"
    cancel = "中断程序"
    while ai.locateOnScreen(image) == None:
        i += 1
        if i >= 10:
            res = ai.confirm(text="找了%s次找到%s" % (i, image),
                             buttons=("%s" % ok, "%s" % cancel))
            if res == ok:
                continue
            else:
                ai.press("k")


def fouceFindImageClick(image, clickPos):
    #judgeImageExists(image)
    time.sleep(0.4)
    clickImage(ai.locateOnScreen(image), clickPos)


#主界面
class MainWindom:
    def __call__(self):
        self._win = tkinter.Tk()
        self._win.wm_attributes('-topmost', 1)
        self._win.title("助手")
        # 大小
        self._win.geometry('350x200+0+600')
        # 按钮
        #b1 = tkinter.Button(self._win, text="连点", command=self.click)
        b1 = tkinter.Button(self._win, text="清空背包", command=self.bagToBox)
        b1.pack(side='left', padx=20)

        b2 = tkinter.Button(self._win, text="出售全部", command=self.doSell)
        b2.pack(side='left', padx=20)

        b3 = tkinter.Button(self._win, text="连点", command=self.doClick)
        b3.pack(side='left', padx=20)
        #截图
        b4 = tkinter.Button(self._win, text="截副手", command=lambda:self.jieTu(fu_shou))
        b4.pack(side='bottom')

        b5 = tkinter.Button(self._win, text="截武器", command=lambda:self.jieTu(wu_qi))
        b5.pack(side='bottom')

        b6 = tkinter.Button(self._win, text="截装备", command=lambda:self.jieTu(zhuan_bei))
        b6.pack(side='bottom')

        b7 = tkinter.Button(self._win, text="截其它", command=lambda:self.jieTu(other))
        b7.pack(side='bottom')

        self._win.mainloop()

    #def click(self):
    #tk = tkinter.Tk()
    #tk.wm_attributes('-topmost', 1)
    #entry = tkinter.Entry(tk, bd=3)
    #entry.bind('<Return>', lambda event:self.doClick(entry, tk))
    #entry.pack(side='right')
    #tk.mainloop()

    #获取买卖订单价差
    def GetPriceDif(self):
        sellPrice = ToolMgr.Read(0, 0)
        buyPrice = ToolMgr.Read(0, 0)
        return int(sellPrice) - int(buyPrice)
    
    def buyOrder(self, x, y):
        #价格框座标
        px = 685
        py = 636

        #创建订单等范围
        createRegion = (800, 696, 969, 797)

        #出售图标范围
        sellRegion = (1211, 389, 1344, 687)

        #点击出售按钮
        #ToolMgr.ClickAndRGB(x, y)
        ToolMgr.ClickAndImage("create.png", 0.9, createRegion, x, y)
        #判断是否已挂单
        if ToolMgr.RGBEqual(1354, 378, 183, 154, 127):
            #回到主界面
            ToolMgr.ClickImageAndImage('sellWDClose.png', 0.9, "sell.png", 0.99, sellRegion)
            return
        
        print(ToolMgr.GetPosRGB(1354, 378))
        print(" no hang")
        #取读取卖单价
        time.sleep(0.5)
        SellPrice = ToolMgr.Read(px, py)
        #点购入订单
        #ToolMgr.ClickAndRGB(609, 542)
        ToolMgr.ClickAndImage("createSellOrder.png", 0.9, createRegion, 609, 542)
        #取买单价
        buyPrice = ToolMgr.Read(px, py)
        #算差价

        diffVale = int(SellPrice) - int(buyPrice)
        #获利小于2万不要
        print(SellPrice)
        print(buyPrice)
        print("diffVale: " + str(diffVale))
        if diffVale < 20000:
            #回到主界面
            #ToolMgr.ClickImageAndImage('sellWDClose.png', 0.9, "bag.png", 0.9)
            ToolMgr.ClickAndImage("create.png", 0.9, createRegion, 615, 516)
            ToolMgr.ClickImageAndImage('create.png', 0.9, "sell.png", 0.99, sellRegion)
            return
        #设置购入订单价
        buyPrice = str(int(buyPrice) + 1)
        ToolMgr.Writer(buyPrice, px, py)
        #点创建按钮
        ToolMgr.ClickImageAndImage('createSellOrder.png', 0.9, 'yes.png', 0.9, (670, 494, 934, 627))
        #点确认提交按键
        ToolMgr.ClickImageAndImage('yes.png', 0.9, 'sell.png', 0.9, sellRegion)

    #循环往复滑动界面
    def LoopScore(self):
        px = 742
        py = 621
        ToolMgr.MoveTo(px, py)
        posRgbArr = ToolMgr.GetAreaRGB(10, 20, px, py)
        ToolMgr.Scroll(-100, 4, px, py)
        pyautogui.sleep(2)
        if ToolMgr.CheckAreaRGB(posRgbArr):
            while True:
                posRgbArr = ToolMgr.GetAreaRGB(10, 20, px, py)
                ToolMgr.Scroll(100, 10)
                pyautogui.sleep(1.5)
                if ToolMgr.CheckAreaRGB(posRgbArr):
                    pyautogui.sleep(120)
                    return
        
    def doClick(self):
        while True:
            sellPosArr = ToolMgr.GetAllImageCenterPos('sell.png', 0.8, 50)
            for pos in sellPosArr:
                self.buyOrder(pos[0], pos[1])
                pyautogui.sleep(0.5)
            self.LoopScore()
            

        return
        print(ToolMgr.RGBEqual(1432, 412, 183, 154, 127))
        strNum = ToolMgr.Read(1392, 664)
        print(strNum)
        num = int(strNum) + 1
        strNum = str(num)
        ToolMgr.Writer(strNum)
    def bagToBox(self):
        return
        initMap()
        JudgeType()
        wear()

    def doSell(self):
        while True:
            ai.click(1282,428)
            time.sleep(0.3)
            ai.click(864,513)
            time.sleep(0.3)
            ai.click(1149,730)
            time.sleep(0.3)
        #while True:
            #fouceFindImageClick(CfgMgr.shared()._sell_name, "centre")
            #fouceFindImageClick(CfgMgr.shared()._sell_type, "centre")
            #fouceFindImageClick(CfgMgr.shared()._sell_yes, "centre")

    def jieTu(self, typeId):
        initMap()
        typeId *= item_id_interval
        x = 1560
        y = 524
        ix = 55
        iy = 49
        t = 82
        image1 = Image.open("%s\%s" %(itemDir, empty_name))
        image1 = make_regalur_image(image1)
        for i in range(5):
            for j in range(4):
                posx = x + j * t
                posy = y + i * t
                while os.path.exists("%s/%s.png" %(itemDir, typeId)):
                    typeId+=1
                newPath = itemDir + "/" + str(typeId) + ".png"
                ai.screenshot(newPath, region=(posx, posy, ix, iy))

                image2 = Image.open(newPath)
                image2 = make_regalur_image(image2)
                if calc_similar(image1, image2) > 0.7:
                    os.remove(newPath)
                    continue
                delSame(newPath, typeId)


class PauseProcess(object):
    def __init__(self):
        self._w_process =None

    def __call__(self):
        #初始化界面
        self.restartWinDow()

        #监听 d, k 键
        with Listener(on_press=self.onPress) as l:
            l.join()

    def onPress(self, key):
        all_key = []
        all_key.append(str(key))
        print(all_key)
        if "'d'" in all_key:
            if self._w_process.status() == 'stopped':
                self._w_process.resume()
            else:
                self._w_process.suspend()
        elif "'k'" in all_key:
            self.restartWinDow()

    def restartWinDow(self):
        if self._w_process:
            self._w_process.terminate()
        win_p = Process(target=MainWindom())
        win_p.start()
        self._w_process = psutil.Process(win_p.pid)

if __name__ == '__main__':
    multiprocessing.freeze_support()
    p_p = Process(target=PauseProcess())
    p_p.start()
    p_p.join()

    #!/usr/bin/python
# -*- coding: UTF-8 -*-

#top = tkinter.Tk()
#L1 = tkinter.Label(top, text="网站名")
#L1.pack(side='left')
#E1 = tkinter.Entry(top, bd=5)
#E1.get()
#E1.bind('<Return>', lambda x:print(E1.get()))
#E1.pack(side='right')

#top.mainloop()
#time.sleep(100)


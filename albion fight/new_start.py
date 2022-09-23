import json
import multiprocessing
import os
import random
import sys
import time
import tkinter
from email.mime import image
from fileinput import filename
from multiprocessing import Process
from tkinter.messagebox import showinfo

import cv2
import matplotlib.image as mpimg
import numpy
import psutil
import pyautogui as ai
from PIL import Image
from pynput.keyboard import Listener

print(os.getcwd())
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

#截地图
mapImage = "mapImage"
newMapFile = ""

#帮助信息
helpInfo = "f1暂停、启动, f2重启"

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
    changeBack(other)
    ai.click(113,204)
    time.sleep(0.5)
    ai.click(113,287)
    time.sleep(0.5)
    ai.click(291,200)

def changeBack(itemType):
    ai.click(151, 271)
    time.sleep(0.5)
    if itemType == wu_qi:
        ai.click(143, 350)
    elif itemType == zhuan_bei:
        ai.click(143, 325)
    elif itemType == fu_shou:
        ai.click(143, 300)
    else:
        ai.click(143, 375)
def JudgeType():
    x = 1560
    y = 524
    ix = 55
    iy = 49
    t = 82
    old_type = 0
    item_type = other

    while True:
        type_info_arr = [] #[idx,posx,poxy]
        ai.click(1814, 452)
        ticks = time.time()
        time.sleep(0.5)
        for i in range(5):
            if item_type == 444:
                break
            for j in range(4):
                posx = x + j * t
                posy = y + i * t
                ai.screenshot("%s\%s" %(itemDir, tmp_item_name), region=(posx, posy, ix, iy))
                item_type = CalSameVal()
                if item_type == error_id:
                    item_type = other
                type_info_arr.append(item_type)
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
                changeBack(txy)
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


class CfgMgr:
    __own = None

    def __init__(self):
        with open('./cfg.json', 'r') as fp:
            cfg = json.load(fp)
        # 移动物体
        self._from_x = cfg['fromX']
        self._from_y = cfg['fromY']
        self._to_x = cfg['toX']
        self._to_y = cfg['toY']
        self._interval_x = cfg['intervalX']
        self._interval_y = cfg['intervalY']
        # 连点
        self._click_interval_tm = cfg['clickIntervalTm']
        # 出售
        self._sell_name = cfg['chuShou']
        self._sell_type = cfg['sellType']
        self._sell_yes = cfg['sellYes']

    @classmethod
    def getOwn(cls):
        return cls.__own

    @classmethod
    def setOwn(cls, own):
        cls.__own = own

    @staticmethod
    def shared():
        if CfgMgr.getOwn() == None:
            CfgMgr.setOwn(CfgMgr())
        return CfgMgr.getOwn()


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


class MainWindom:
    def __call__(self):
        self._win = tkinter.Tk()
        self._win.wm_attributes('-topmost', 1)
        self._win.title("ablion")
        # 大小
        self._win.geometry('300x150+0+0')
        # 按钮
        b1 = tkinter.Button(self._win, text="帮忙信息", command=lambda:showinfo(message=helpInfo))
        #b1.pack(side='left', padx=20)
        b1.grid(row = 0, column=0, pady=5, padx=5)

        b2 = tkinter.Button(self._win, text="出售全部", command=self.doSell)
        b2.grid(row = 0, column=1, pady=5, padx=5)

        b3 = tkinter.Button(self._win, text="连点", command=self.doClick)
        b3.grid(row = 0, column=2, pady=5, padx=5)
        #截图
        b4 = tkinter.Button(self._win, text="截副手", command=lambda:self.jieTu(fu_shou))
        b4.grid(row = 0, column=3, pady=5, padx=5)

        b5 = tkinter.Button(self._win, text="截武器", command=lambda:self.jieTu(wu_qi))
        b5.grid(row = 1, column=0, pady=5, padx=5)

        b6 = tkinter.Button(self._win, text="截装备", command=lambda:self.jieTu(zhuan_bei))
        b6.grid(row = 1, column=1, pady=5, padx=5)

        b7 = tkinter.Button(self._win, text="截其它", command=lambda:self.jieTu(other))
        b7.grid(row = 1, column=2, pady=5, padx=5)

        b8 = tkinter.Button(self._win, text="清空背包", command=self.doMove)
        b8.grid(row = 1, column=3, pady=5, padx=5)

        b9 = tkinter.Button(self._win, text="截地图", command=lambda:self.jieMap())
        b9.grid(row = 2, column=0, pady=5, padx=5)

        b10 = tkinter.Button(self._win, text="打开截地图", command=lambda:self.openJieMap())
        b10.grid(row = 2, column=1, pady=5, padx=5)

        self._win.mainloop()

    def doClick(self):
        while True:
            ai.click()
            #time.sleep(float(CfgMgr.shared()._click_interval_tm))

    def doMove(self):
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

    def jieMap(self):
        print(os.getcwd())
        global newMapFile
        newMapFile = time.strftime("%Y%m%d%H%M%S", time.localtime()) + ".png"
        ai.screenshot(r"%s\%s" %(mapImage, newMapFile), region=(0, 0, 100, 100))
        #ai.screenshot(r"%s\%s" %("D:\git data\python\mapImage", newMapFile), region=(0, 0, 100, 100))

    def openJieMap(self):
        if newMapFile == "":
            self.jieMap()
        im = Image.open(r"%s\%s" %(mapImage, newMapFile))
        im.show()

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
        self.restartWin()
        with Listener(on_press=self.onPress) as l:
            l.join()

    def onPress(self, key):
        all_key = []
        all_key.append(str(key))
        print(all_key)
        if "Key.f1" in all_key:
            if self._w_process.status() == 'stopped':
                self._w_process.resume()
            else:
                self._w_process.suspend()
        elif "Key.f2" in all_key:
            self.restartWin()

    def restartWin(self):
        if self._w_process:
            self._w_process.terminate()
        win_p = Process(target=MainWindom())
        win_p.start()
        self._w_process = psutil.Process(win_p.pid)

if __name__ == '__main__':
    ##ai.screenshot(newPath, region=(posx, posy, ix, iy))
    #time_str_new = time.strftime("%Y%m%d-%H:%M:%S", time.localtime())
    ##ai.screenshot(newPath, region=(posx, posy, ix, iy))
    #print(time_str_new)

    #image1 = Image.open(r"D:\\git data\\python\\albion fight\\1.jpg")
    ##image1.show("safa")

    #image1.show()

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


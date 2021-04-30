import json
import os
import random
import sys
import time
import tkinter
from multiprocessing import Process
import multiprocessing
import psutil
import pyautogui as ai
from pynput.keyboard import Listener


def randomFloat(num, half=0):
    if half == 0:
        half = num / 2
    return random.uniform(num - half, num + half)


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
    judgeImageExists(image)
    clickImage(ai.locateOnScreen(image), clickPos)


class MainWindom:
    def __call__(self):
        self._win = tkinter.Tk()
        self._win.wm_attributes('-topmost', 1)
        self._win.title("助手")
        # 大小
        self._win.geometry('300x200+0+0')
        # 按钮
        #b1 = tkinter.Button(self._win, text="连点", command=self.click)
        b1 = tkinter.Button(self._win, text="清空背包", command=self.doMove)
        b1.pack(side='left', padx=20)

        b2 = tkinter.Button(self._win, text="出售全部", command=self.doSell)
        b2.pack(side='left', padx=20)

        b3 = tkinter.Button(self._win, text="连点", command=self.doClick)
        b3.pack(side='left', padx=20)

        self._win.mainloop()

    #def click(self):
    #tk = tkinter.Tk()
    #tk.wm_attributes('-topmost', 1)
    #entry = tkinter.Entry(tk, bd=3)
    #entry.bind('<Return>', lambda event:self.doClick(entry, tk))
    #entry.pack(side='right')
    #tk.mainloop()

    def doClick(self):
        while True:
            ai.click()
            time.sleep(float(CfgMgr.shared()._click_interval_tm))

    def doMove(self):
        fx = CfgMgr.shared()._from_x
        fy = CfgMgr.shared()._from_y
        tx = CfgMgr.shared()._to_x
        ty = CfgMgr.shared()._to_y
        ix = CfgMgr.shared()._interval_x
        iy = CfgMgr.shared()._interval_y
        for y in range(0, 3):
            for x in range(0, 3):
                ai.moveTo(fx + ix * x, fy + iy * y, 0.2)
                ai.dragTo(tx, ty, 0.2, button='left')

    def doSell(self):
        while True:
            fouceFindImageClick(CfgMgr.shared()._sell_name, "centre")
            fouceFindImageClick(CfgMgr.shared()._sell_type, "centre")
            fouceFindImageClick(CfgMgr.shared()._sell_yes, "centre")


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
        if "'d'" in all_key:
            if self._w_process.status() == 'stopped':
                self._w_process.resume()
            else:
                self._w_process.suspend()
        elif "'k'" in all_key:
            self.restartWin()

    def restartWin(self):
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
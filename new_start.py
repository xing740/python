from multiprocessing import Process
from pynput.keyboard import Listener
import time
import tkinter
import os
import psutil
import sys
import pyautogui as ai
import random

def randomFloat(num, half=0):
    if half == 0:
        half = num / 2
    return random.uniform(num - half, num + half)

def randomInt(num, half=0):
    if half == 0:
        half = num / 2
    left = num - half if num - half > 1 else 1
    return random.randint(int(left), int(num + half))

class MainWindom:
    def __call__(self):
        self._win = tkinter.Tk()
        self._win.wm_attributes('-topmost', 1)
        self._win.title("助手")
        # 大小
        self._win.geometry('300x200+0+0')
        # 按钮
        #b1 = tkinter.Button(self._win, text="连点", command=self.click)
        b1 = tkinter.Button(self._win, text="连点", command=self.doMove)
        b1.pack(side='left', padx=20)

        b2 = tkinter.Button(self._win, text="b2", command=self.button2)
        b2.pack(side='right', padx=20)

        self._win.mainloop()

    def click(self):
        tk = tkinter.Tk()
        tk.wm_attributes('-topmost', 1)
        entry = tkinter.Entry(tk, bd=3)
        entry.bind('<Return>', lambda event:self.doClick(entry, tk))
        entry.pack(side='right')
        tk.mainloop()

    def doClick(self, entry, tk):
        str_sec = entry.get()
        if str_sec != None and str_sec.isdigit() == False:
            str_sec = 0.5

        str_sec = float(str_sec) if str_sec != None else 0.5
        while True:
            ai.click()
            time.sleep(str_sec)
        tk.destroy()

    def doMove(self):
        fx = 35
        fy = 29
        tx = 590
        ty = 39
        ix = 82
        iy = 101
        for y in range(0, 3):
            for x in range(0, 3):
                ai.moveTo(fx + ix * x, fy + iy * y, 0.2)
                ai.dragTo(tx, ty, 0.2, button='left')


    def button2(self):
        for i in range(10, 20):
            print(i)

class PauseProcess(object):
    def __init__(self):
        self._w_process = None

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
    #p_p = Process(target=PauseProcess())
    #p_p.start()
    #p_p.join()



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
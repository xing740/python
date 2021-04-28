from pynput.keyboard import Listener
import time
import tkinter
import os
from multiprocessing import Process
import psutil


# 设置进程1，实现目标：按键监听，当按下“d”键时，进程2能挂起（暂停运行），并弹窗提示"继续程序"和"终止程序"按钮。
# 当按下"继续程序"按钮时，进程2能接下去运行，当按下"终止程序"时，进程2能结束运行。
def work1(pid, mainpid):
    # 按键监听，当按下“d"键时弹窗
    def on_press(key):
        all_key = []
        all_key.append(str(key))
        if "'d'" in all_key:
            pause = psutil.Process(pid)  # 传入子进程的pid
            pause.suspend()  # 暂停子进程
            print(f'{pid}子进程已暂停。。。。')

    def on_release(key):
        all_key = []
        all_key.append(str(key))
        if "'d'" in all_key:
            def zzcx():
                pipause = psutil.Process(mainpid)  # 传入主进程的pid
                pipause.kill()
                print(f'{mainpid}主进程已结束。。。。')
                tanchuan_zt.destroy()

            def jxcx():
                pause = psutil.Process(pid)  # 传入子进程的pid
                pause.resume()  # 暂停子进程
                print(f'{pid}子进程已继续。。。。')

            tanchuan_zt = tkinter.Tk()
            tanchuan_zt.wm_attributes('-topmost', 1)
            tanchuan_zt.title("终止/暂停程序")
            tkinter.wb_zt = tkinter.Label(tanchuan_zt, text="您按下了”D(d)“键，此为暂停程序键，\n请问是否继续", compound=tkinter.CENTER,
                          font=("楷体", 20), fg="black")
            tkinter.wb_zt.pack(pady=20)
            xx1_button = tkinter.Button(tanchuan_zt, text="终止程序", command=zzcx)
            xx1_button.pack(side="left", padx=120)
            xx2_button = tkinter.Button(tanchuan_zt, text="继续程序", command=jxcx)
            xx2_button.pack(side="right", padx=120)

            # 弹窗位置大小设置
            width = 700
            height = 200
            screenwidth = tanchuan_zt.winfo_screenwidth()
            screenheight = tanchuan_zt.winfo_screenheight()
            alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
            tanchuan_zt.geometry(alignstr)
            tanchuan_zt.mainloop()

            all_key.clear()  # 对列表进行清空

        # if key == Key.esc:  # 停止监听
        #     return Falseurn False

    def start_listen():  # 设置监听
        with Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()

    start_listen()  # 启动监听


# 设置进程2，一个普通的打印数字程序
def work2():
    for i in range(1, 10000):
        print('x' + str(i))
        time.sleep(1)


if __name__ == '__main__':
    mainpid = os.getpid()  # 获取主进程pid
    p2 = Process(target=work2)
    p2.start()
    pid = p2.pid  # 获取子进程pid
    p1 = Process(target=work1, args=(pid, mainpid))
    p1.start()

    p1.join()
    p2.join()

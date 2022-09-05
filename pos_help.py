from turtle import position

import pyautogui as ai
from pynput.mouse import Listener

x = 0
y = 0
def do(a1, a2, a3, a4):
    global x
    global y
    pos = ai.position()
    print(pos)
    print(str(pos.x - x) + " " + str(pos.y - y))
    x = pos.x
    y = pos.y

if __name__ == '__main__':
    with Listener(on_click=do) as l:
        l.join()

\\94 36
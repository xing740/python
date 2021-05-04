import pyautogui as ai
from pynput.mouse import Listener

def do(a1, a2, a3, a4):
    print(ai.position())

if __name__ == '__main__':
    with Listener(on_click=do) as l:
        l.join()
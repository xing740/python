import pyautogui
import time

while True:
    time.sleep(0.2)
    m = pyautogui.position()
    pyautogui.click(m.x, m.y)
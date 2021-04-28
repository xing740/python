#!/usr/bin/python
#coding:utf-
from pymouse import PyMouse
from pykeyboard import PyKeyboard
from PIL import Image
import pytesseract

m = PyMouse()
k = PyKeyboard()

x_dim, y_dim = m.screen_size()
#m.click(500, 500)
#k.type_string('Hello, World!')
Image = Image.open('1.png')
text = pytesseract.image_to_string(Image, lang='chi_sim')
print(text)
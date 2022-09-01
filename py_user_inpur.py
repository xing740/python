#!/usr/bin/python
#coding:utf-

import pytesseract
from PIL import Image
from pykeyboard import PyKeyboard
from pymouse import PyMouse

m = PyMouse()
k = PyKeyboard()

x_dim, y_dim = m.screen_size()
#m.click(500, 500)
#k.type_string('Hello, World!')
Image = Image.open('18.png')
text = pytesseract.image_to_string(Image,lang='eng')
print(text)


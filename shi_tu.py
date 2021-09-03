# -*- coding: utf-8 -*-
# !/usr/bin/env python
# @Time    : 2018/11/17 16:04
# @Author  : xhh
# @Desc    : 通过直方图计算图片的相似度
# @File    : difference_image_hist.py
# @Software: PyCharm
from PIL import Image
import pyautogui as ai
import os
from enum import Enum
import time
import sys

tmp_item_name = "9999.png"
empty_name = "10000.png"
valMap = {}
ids = []

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
                sys.exists()
def fouceFindImageClick(image, clickPos):
    judgeImageExists(image)
    clickImage(ai.locateOnScreen(image), clickPos)
 
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

item_id_interval = 1000
wu_qi = 1
zhuan_bei = 2
fu_shou = 3
other = 4
empty_id = 5
error_id = 6

itemDir = "items"
def jie_tu(typeId):
    typeId *= item_id_interval
    x = 1560
    y = 524
    ix = 55
    iy = 49
    t = 82
    image1 = Image.open("%s\%s" %(itemDir, empty_name))
    image1 = make_regalur_image(image1)
        #image2 = Image.open("%s\%s" %(itemDir, it))
        #image2 = make_regalur_image(image2)
        image2 = valMap.get(it)
        if image2 == None:
            continue
        val = calc_similar(image1, image2)
        if val >= 0.65:
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

def JudgeType():
    x = 1560
    y = 524
    ix = 55
    iy = 49
    t = 82
    old_type = 0
    while True:
        ai.click(1814, 452)
        time.sleep(1)
        for i in range(5):
            for j in range(4):
                posx = x + j * t
                posy = y + i * t
                ai.screenshot("%s\%s" %(itemDir, tmp_item_name), region=(posx, posy, ix, iy))
                item_type = CalSameVal()
                if item_type == error_id:
                    continue
                if item_type == empty_id:
                    ai.keyUp("shift")
                    return
                print("type:"+str(item_type))
                if item_type != old_type:
                    changeBack(item_type)
                    old_type = item_type
                ai.keyDown("shift")
                ai.moveTo(posx + ix / 2, posy + iy / 2)
                ai.mouseDown()
                ai.mouseUp()
                ai.mouseDown()
                ai.mouseUp()
                ai.keyUp("shift")

def initMap():
    tmp = os.listdir(itemDir)
    for it in tmp:
        ids.append(it)
        if it == tmp_item_name:
            continue
        image2 = Image.open("%s\%s" %(itemDir, it))
        valMap[it] = make_regalur_image(image2)
    print(valMap)

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
        if val >= 0.65:
            print("val:"+ str(val)+" itemId:"+str(it))
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

def fixAll():
    #fouceFindImageClick("jie_tu/weiXiu.png", "center")
    fouceFindImageClick("jie_tu/yes.png", "center")
    fouceFindImageClick("jie_tu/give.png", "center")
    fouceFindImageClick("jie_tu/overGive.png", "center")
    fouceFindImageClick("jie_tu/box.png", "center")
    judgeImageExists("jie_tu/boxOpen.png")

def doSell():
    time.sleep(3)
    for i in range(100):
        ai.click(1282,428)
        time.sleep(0.1)
        ai.click(864,513)
        time.sleep(0.1)
        ai.click(1149,730)
        time.sleep(0.1)

if __name__ == '__main__':
    #image1 = Image.open('shi_tu1.png')
    #image1 = make_regalur_image(image1)
    #image2 = Image.open('shi_tu.2.png')
    #image2 = make_regalur_image(image2)
    #print("图片间的相似度为",calc_similar(image1, image2))
    #jie_tu(other)
    #fixAll()

    initMap()
    JudgeType()
    wear()

    #doSell()
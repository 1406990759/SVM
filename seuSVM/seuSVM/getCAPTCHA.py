#coding=utf8
import requests
import threading
import sys
from sgmllib import SGMLParser
reload(sys)
sys.setdefaultencoding('utf8')

imgurl = 'http://my.seu.edu.cn/captchaGenerate.portal?s=0.8661741290707141'
path = "login\\"
list_th = []

def getCAPTCHA():
    global imgurl,path
    r = requests.get(imgurl)
    img = r.content
    imgName = "login.jpg"
    with open(path+imgName , 'wb') as pic:
        pic.write(img)

def getManyCAPTCHA():
    global imgurl,path
    for i in range(1000):
        r = requests.get(imgurl)
        img = r.content
        imgName = "%d.jpg" %i
        with open(path+imgName , 'wb') as pic:
            pic.write(img)

#getManyCAPTCHA()
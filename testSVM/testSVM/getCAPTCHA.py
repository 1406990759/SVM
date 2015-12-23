#coding=utf8
import requests
import threading
import sys
from sgmllib import SGMLParser
reload(sys)
sys.setdefaultencoding('utf8')

imgurl = 'http://xk.urp.seu.edu.cn/studentService/getCheckCode'
path = "login\\"
list_th = []

def getCAPTCHA():
    global imgurl,path
    r = requests.get(imgurl)
    img = r.content
    imgName = "login.jpg"
    with open(path+imgName , 'wb') as pic:
        pic.write(img)

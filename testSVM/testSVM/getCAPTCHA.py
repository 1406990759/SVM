#coding=utf8
import requests
import threading
import sys
from sgmllib import SGMLParser
reload(sys)
sys.setdefaultencoding('utf8')

imgurl = 'http://xk.urp.seu.edu.cn/jw_css/getCheckCode'
path = "img\\"
list_th = []

def getCAPTCHA(num):
    global imgurl,path
    for i in range(num,num+100):
        print i
        r = requests.get(imgurl)
        img = r.content
        imgName = str(i) + ".jpg"
        with open(path+imgName , 'wb') as pic:
            pic.write(img)


for i in range(10):
    th = threading.Thread(target=getCAPTCHA,args=(i*100,))
    th.start()
    list_th.append(th)
for th in list_th:
    th.join()

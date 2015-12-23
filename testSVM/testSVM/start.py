from divide import *
from train import *
from getCAPTCHA import *
import requests
from sgmllib import SGMLParser
#while True:
#    x = int(input())
#    s = ""
#    image_arr = handle(x)
#    XX = []
#    BLACK = (0,0,0)
#    WHITE = (255,255,255)
#    for img in image_arr:
#        pixdata = img.load()
#        width,height = img.size
#        data = []
#        for i in xrange(width):
#            for j in xrange(height):
#                if pixdata[i,j] == BLACK:
#                    data.append(0)
#                else:
#                    data.append(1)
#        XX.append(data)
#    print clf.predict(XX)

username = '213130798'
password = 'a3676677'


getCAPTCHA()
image_arr = handleCAPTCHA('login\\login.jpg')
XX = []
BLACK = (0,0,0)
WHITE = (255,255,255)
for img in image_arr:
    pixdata = img.load()
    width,height = img.size
    data = []
    for i in xrange(width):
        for j in xrange(height):
            if pixdata[i,j] == BLACK:
                data.append(0)
            else:
                data.append(1)
    XX.append(data)
#for i in clf.predict(XX):

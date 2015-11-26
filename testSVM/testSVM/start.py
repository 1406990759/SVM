from divide import *
from train import *
while True:
    x = int(input())
    s = ""
    image_arr = handle(x)
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
    print clf.predict(XX)
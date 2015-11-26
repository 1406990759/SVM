#coding=utf-8
import sys
import copy
from PIL import Image
reload(sys)
sys.setdefaultencoding('utf8')
# 切割字符
def cut(img,i):
    width,height = img.size
    BLACK = (0,0,0)
    WHITE = (255,255,255)
    pixdata = img.load()
    pic_arr = []
    for k in range(4):
        high = 0
        for j in xrange(height):
            for n in xrange(50*k,50*(k+1)):
                if pixdata[n,j] == BLACK:
                    high = j
                    break
            if high != 0:
                break
        box = (50*k,high,50*(k+1),high + 50)
        xim = img.crop(box)
        xim.save('test\\%d_%d.bmp'%(i,k))
        pic_arr.append(xim)
    return pic_arr
# 中值滤波
def remove_noise(img,window=1):
    window_x = []
    window_y = []
    if window == 1:
        # 十字形
        window_x = [1,0,0,-1,0]
        window_y = [0,1,0,0,-1]
    elif window == 2:
        # 3*3矩阵型
        window_x = [-1,0,1,-1,0,1,1,-1,0]
        window_y = [-1,-1,-1,1,1,1,0,0,0]
    elif window == 3:
        # 5*5矩阵型
        for i in range(-2,3):
            for j in range(-2,3):
                window_x.append(i)
                window_y.append(j)

    width,height = img.size
    pixdata = img.load()
    BLACK = (0,0,0)
    WHITE = (255,255,255)
    color = [WHITE,BLACK]
    temp = []

    for i in xrange(width):
        temp.append([])
        for j in xrange(height):
            box = []
            jump = False
            black_count,white_count = 0,0
            for k in xrange(len(window_x)):
                d_x = i + window_x[k]
                d_y = j + window_y[k]
                try:
                    if pixdata[d_x, d_y] == color[1]:
                        box.append(1)
                    else:
                        box.append(0)
                except IndexError:
                    pixdata[i,j] = color[0]
                    #temp[i].append(color[0]) 
                    jump = True
                    break
            box.sort()
            if jump == False: 
                pixdata[i,j] = color[box[(len(box))/2]]
# 直线清理
def clean(img):
    width,height = img.size
    BLACK = (0,0,0)
    WHITE = (255,255,255)
    pixdata = img.load()
    for i in xrange(width):
        count = 0
        c_count = 0
        s_count = 0
        flag = False
        for j in xrange(height):
            if i > 0 and i < width - 1:
                if pixdata[i-1,j] == WHITE and pixdata[i+1,j] == WHITE:
                    pixdata[i,j] = WHITE
            elif i == 0 and pixdata[i+1,j] == WHITE:
                pixdata[i,j] = WHITE
            elif i == width-1 and pixdata[i-1,j] == WHITE:
                pixdata[i,j] == WHITE

            if pixdata[i,j] == BLACK:
                count += 1
                flag = True
            elif count != 0:
                if flag == True:
                    c_count += 1
                    s_count = count
                    flag = False
                if count <= 5:
                    for k in range(count):
                        pixdata[i,j-k-1] = WHITE
                count = 0
        if c_count == 1 and s_count < 10:
            for j in xrange(height):
                pixdata[i,j] = WHITE
# 小团去噪
def fix(img):
    width,height = img.size
    BLACK = (0,0,0)
    WHITE = (255,255,255)
    pixdata = img.load()
    kind = 0
    kind_a = []
# 二值化
def binaryzation(img, threshold=30):
    BLACK = (0,0,0)
    WHITE = (255,255,255)
    width,height = img.size
    pixdata = img.load()
    for i in xrange(width):
        for j in xrange(height):
            r,g,b = pixdata[i,j]
            if r > threshold or g > threshold or b > threshold:
                pixdata[i,j] = WHITE
            else:
                pixdata[i,j] = BLACK
# 处理过程
def prehandle():
    for i in range(25,125):
        img = Image.open('img\\%d.jpg'%i)
        #img = img.convert("RGBA")
        binaryzation(img,30)
        clean(img)
        remove_noise(img,3)
        #img.show()
        img.save('clean\\%d.bmp'%i)
        cut(img,i)
        print u'第%d个处理完成'%i
def handle(num):
    img = Image.open('img\\%d.jpg'%num)
    binaryzation(img,30)
    clean(img)
    remove_noise(img,3)
    img.save('clean\\%d.bmp'%num)
    return cut(img,num)

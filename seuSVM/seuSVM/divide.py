#coding=utf-8
import sys
from PIL import Image
reload(sys)
sys.setdefaultencoding('utf8')
# 切割字符
def cut(img,i):
    width,height = img.size
    BLACK = (0,0,0)
    WHITE = (255,255,255)
    pixdata = img.load()
    edge = []
    top = []
    pic_arr = []
    
    ############ 判断左右边界 ##############
    judge = 0
    for n in xrange(width):
        count = 0
        for j in xrange(height):
            if judge == 0 and pixdata[n,j] == BLACK:
                edge.append(n)
                judge = 1
                count = 1
                break
            if judge == 1 and pixdata[n,j] == BLACK:
                count += 1
        if judge == 1 and count == 0:
            edge.append(n-1)
            judge = 0
    if len(edge) == 7:
        edge.append(width-1)
    
    ############ 判断上下边界 ##############

    for k in range(4):
        judge = 0
        for j in xrange(height):
            count = 0
            for n in xrange(edge[2*k],edge[2*k+1]+1):
                if judge == 0 and pixdata[n,j] == BLACK:
                    top.append(j)
                    judge = 1
                    count = 1
                    break
                if judge == 1 and pixdata[n,j] == BLACK:
                    count += 1
            if judge == 1 and count == 0:
                top.append(j-1)
                break
        box = (edge[2*k],top[2*k],edge[2*k+1]+1,top[2*k+1])
        xim = img.crop(box)
        xim.save('cut\\%d_%d.bmp'%(i,k))
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
    for i in range(100,200):
        img = Image.open('img\\%d.jpg'%i)
        binaryzation(img,30)
        remove_noise(img,2)
        cut(img,i)
        print u'第%d个处理完成'%i

def handle(num):
    img = Image.open('login\\%d.jpg'%num)
    binaryzation(img,30)
    remove_noise(img,2)
    cut(img,num)
    return cut(img,num)

def handleCAPTCHA(path):
    img = Image.open(path)
    binaryzation(img,30)
    return cut(img,0)

#prehandle()

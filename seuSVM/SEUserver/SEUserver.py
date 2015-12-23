#coding=utf8
import requests
import os
import threading
from sklearn import svm
from sklearn import cross_validation
from sklearn.metrics import classification_report
from PIL import Image
import sys
from sgmllib import SGMLParser
reload(sys)
sys.setdefaultencoding('utf8')

class identityCAPTCHA():
    # 初始化 pic默认名字login.jpg
    def __init__(self, url, name = 'login'):
        self.url = url
        self.name = name
        self.trainX = []
        self.trainY = []
    # 存放验证码至img文件夹中
    def getCAPTCHA(self):
        r = requests.get(self.url)
        with open('img\\%s.gif'%self.name, 'wb') as pic:
            pic.write(r.content)
        self.img = Image.open('img\\%s.gif'%self.name)
        self.img = self.img.convert('RGB')        
    # 切割字符
    def cut(self):
        i = self.name
        width,height = self.img.size
        BLACK = (0,0,0)
        WHITE = (255,255,255)
        pixdata = self.img.load()
        edge = []
        top = []
        pic_arr = []
    
        ############ 判断左右边界 ##############
        judge = 0
        for n in xrange(1,width-1):
            count = 0
            for j in xrange(1,height-1):
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
            for j in xrange(1,height):
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
            box = (edge[2*k],top[2*k],edge[2*k] + 8,top[2*k] + 10)
            xim = self.img.crop(box)
            #xim.save('cut\\%s_%d.bmp'%(i,k))
            pic_arr.append(xim)
        return pic_arr
    # 中值滤波
    def remove_noise(self, window=1):
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

        width,height = self.img.size
        pixdata = self.img.load()
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
    def binaryzation(self, threshold=30):
        BLACK = (0,0,0)
        WHITE = (255,255,255)
        width,height = self.img.size
        pixdata = self.img.load()
        for i in xrange(width):
            for j in xrange(height):
                r,g,b = pixdata[i,j]
                if r > threshold or g > threshold or b > threshold:
                    pixdata[i,j] = WHITE
                else:
                    pixdata[i,j] = BLACK
    # 处理过程
    def handle(self, name):
        self.name = name
        self.getCAPTCHA()
        self.binaryzation(30)
        return self.cut()
    # 获取大量训练集
    def getMany(self):
        for i in range(100):
            self.handle(str(i))
    # 遍历指定目录，显示目录下的所有文件名并读取到训练集trainX，trainY中
    def eachFile(self, filepath):
        pathDir =  os.listdir(filepath)
        BLACK = (0,0,0)
        WHITE = (255,255,255)
    
        for allDir in pathDir:
            image = Image.open(filepath+allDir)
            width,height = image.size
            pixdata = image.load()
            data = []
            for i in xrange(height):
                for j in xrange(width):
                    if pixdata[j,i] == BLACK:
                        data.append(0)
                    else:
                        data.append(1)
            self.trainX.append(data)
            self.trainY.append(str(filepath[-2:-1]))
    # 使用SVM训练训练集
    def SVM(self):
        for i in "0123456789":
            path = 'cut\\%s\\'%i
            self.eachFile(path)
        self.clf = svm.SVC(gamma = 0.01, C = 1.0)
        X_tr, X_tt, y_tr, y_tt = cross_validation.train_test_split(self.trainX, self.trainY, test_size = 0.2, random_state = 0)
        self.clf.fit(X_tr, y_tr)
        y_true, y_pred = y_tt, self.clf.predict(X_tt)
        print(classification_report(y_true, y_pred))
    # 预测
    def predict(self):
        image_arr = self.handle('predict')
        XX = []
        BLACK = (0,0,0)
        WHITE = (255,255,255)
        for img in image_arr:
            pixdata = img.load()
            width,height = img.size
            data = []
            for i in xrange(height):
                for j in xrange(width):
                    if pixdata[j,i] == BLACK:
                        data.append(0)
                    else:
                        data.append(1)
            XX.append(data)
        print self.clf.predict(XX)



imgurl = 'https://selfservice.seu.edu.cn/selfservice/verifyCode.php'

iden = identityCAPTCHA(imgurl)

iden.SVM()
iden.predict()
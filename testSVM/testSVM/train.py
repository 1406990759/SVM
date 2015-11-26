#coding=utf-8
import sys
import os
import copy
from sklearn import svm
from sklearn import cross_validation
from sklearn.metrics import classification_report
from PIL import Image
reload(sys)
sys.setdefaultencoding('utf8')

X = []
Y = []
# 遍历指定目录，显示目录下的所有文件名
def eachFile(filepath):
    pathDir =  os.listdir(filepath)
    BLACK = (0,0,0)
    WHITE = (255,255,255)
    
    for allDir in pathDir:
        image = Image.open(filepath+allDir)
        width,height = image.size
        pixdata = image.load()
        data = []
        for i in xrange(width):
            for j in xrange(height):
                if pixdata[i,j] == BLACK:
                    data.append(0)
                else:
                    data.append(1)
        X.append(data)
        Y.append(int(filepath[-2:-1]))

def getData():
    for i in range(10):
        path = 'test\\%d\\'%i
        eachFile(path)

getData()
#SVM Classifier  
clf = svm.SVC(gamma = 0.001, C = 1.0)
X_tr, X_tt, y_tr, y_tt = cross_validation.train_test_split(X, Y, test_size = 0.1, random_state = 0)
clf.fit(X_tr, y_tr)
y_true, y_pred = y_tt, clf.predict(X_tt)

print(classification_report(y_true, y_pred))
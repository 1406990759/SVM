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
        for i in xrange(height):
            for j in xrange(width):
                if pixdata[j,i] == BLACK:
                    data.append(0)
                else:
                    data.append(1)
        X.append(data)
        Y.append(str(filepath[-2:-1]))
    #print i
def getData():
    for i in "2345678bcdefmnpwxy":
        path = 'train\\%s\\'%i
        eachFile(path)

getData()
for i in range(len(X)):
    l = len(X[i])
    X[i].extend([1]*(3500-l))
        
        
#print m
#SVM Classifier  
clf = svm.SVC(gamma = 0.0008, C = 1.0)
X_tr, X_tt, y_tr, y_tt = cross_validation.train_test_split(X, Y, test_size = 0.2, random_state = 0)
clf.fit(X_tr, y_tr)
y_true, y_pred = y_tt, clf.predict(X_tt)

print(classification_report(y_true, y_pred))
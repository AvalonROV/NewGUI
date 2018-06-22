import sys
import os
import math
import cv2
import numpy as np

from math import *
from PyQt4 import QtGui, QtCore


#https://uk.mathworks.com/help/vision/ref/undistortimage.html
# http://www.tannerhelland.com/4743/simple-algorithm-correcting-lens-distortion/
#https://stackoverflow.com/questions/11790504/about-a-pyqt-example-program
#I THINK I SHOULD CREATE SEPRATE BOXES FOR PROCESS INFORMATION AND SEND INFORMATION

class Example(QtGui.QWidget):  
      
    def __init__(self):
        super(Example, self).__init__()
         
        self.textBox()
        
        self.y_cordinate=0
        self.x_cordinate=0
        self.X2=0
        self.Y2=0
        self.X_Coordinate=0
        self.new_X=0
        self.new_Y=0
        self.RequiredDistance_1=0
        self.pipe_multiplier=1
        self.roi = np.loadtxt("mtx.txt", dtype='i', delimiter=',')
        self.newcameramtx = np.loadtxt("cameraMatrix.txt", dtype='i', delimiter=',')
        self.dist = np.loadtxt("dist.txt", dtype='i', delimiter=',')
        self.mtx = np.loadtxt("mtx.txt", dtype='i', delimiter=',')
        
        self.setGeometry(300, 200, 1000, 500)
        self.setWindowTitle('TASK 3')  
        self.buttonStore1()
 
        
        self.btn.clicked.connect(self.StoreValue1)
        self.btn1.clicked.connect(self.StoreValue2)
        self.btn2.clicked.connect(self.Calculate)
        self.btn3.clicked.connect(self.SlopeCalculate)
        self.btn4.clicked.connect(self.click)
 
        self.show()
    
    def mouseReleaseEvent(self, QMouseEvent):
        cursor =QtGui.QCursor()
        current=QtGui.QWidget.mapFromGlobal(self,cursor.pos())
        self.x_cordinate = current.x()
        self.y_cordinate = current.y()
    
    def buttonStore1(self):
        self.btn=QtGui.QPushButton("Press for First Point",self)
        #self.btn.resize(100,50)
        self.btn.adjustSize()
        self.btn.move(700,150)
        self.btn.setStyleSheet("QPushButton { background-color: white }""QPushButton:pressed { background-color: lightgreen }" )
        
        self.btn1=QtGui.QPushButton("Press for Second Point",self)
        #self.btn1.resize(100,50)
        self.btn1.adjustSize()
        self.btn1.move(700,200)
        self.btn1.setStyleSheet("QPushButton { background-color: white }""QPushButton:pressed { background-color: lightgreen }" )
   
        self.btn2=QtGui.QPushButton("RESULT",self)
        self.btn2.adjustSize()
#        self.btn2.resize(100,50)
        self.btn2.move(800,350)
        self.btn2.setStyleSheet("QPushButton { background-color: white }""QPushButton:pressed { background-color: lightgreen }" )

        self.btn3=QtGui.QPushButton("Slope",self)
        self.btn3.adjustSize()
#        self.btn3.resize(100,50)
        self.btn3.move(700,350)
        self.btn3.setStyleSheet("QPushButton { background-color: white }""QPushButton:pressed { background-color: lightgreen }" )
        
        self.btn4=QtGui.QPushButton("Enter and Press for Required Distance",self)
        self.btn4.adjustSize()
#        self.btn4.resize(50,50)
        self.btn4.move(700,70)
        self.btn4.setStyleSheet("QPushButton { background-color: white }""QPushButton:pressed { background-color: lightgreen }" )
        self.show()
        
    def textBox(self):
        self.textbox = QtGui.QLineEdit(self)
        self.textbox.move(700, 30)
        self.textbox.resize(100,30)
        
    def click(self):
        self.RequiredDistance=float(self.textbox.text())
        print(self.RequiredDistance)
        
    def Calculate(self): # Assumes that the x-cordinate is constant
        objectDistance=math.sqrt((self.X2-self.X1)**2 + ((self.Y2-self.Y1)**2)) # This is a more accurate way to calculate distance than Y2-Y1
#       print(objectDistance)
        actualDistance=42
        scale=actualDistance/(objectDistance)
        X_ReferenceObject=self.X2
#        self.X_Coordinate = (self.RequiredDistance/scale)+ X_ReferenceObject
#        print(self.X_Coordinate)
#        QtGui.QWidget.update(self,self.X2,self.Y2, self.rect().width() -self.X_Coordinate , self.Y2)
        self.X_Coordinate = X_ReferenceObject + (self.RequiredDistance/scale)
#        self.radius=(self.X_Coordinate-self.X2)*(math.cos(self.angle))
        #IS RADIUS X2_COORDINATE-X2 OR USING THE RADIUS METHOD???
        self.new_X=self.X2+self.pipe_multiplier*((self.X_Coordinate-self.X2)*math.cos(self.angle)) 
        self.new_Y=self.Y2-self.pipe_multiplier*((self.X_Coordinate-self.X2)*math.sin(self.angle))
        print(self.new_Y)
        print(self.new_X)
        QtGui.QWidget.update(self)
        
    def SlopeCalculate(self):
        self.slope=(self.Y1-self.Y2)/(self.X2-self.X1)#Y1-Y2 as the Y Axis start from top and move to bottom so sign was reversed
        self.pipe_orientation= (self.X2-self.X1)
        if(self.pipe_orientation>0):
            self.pipe_multiplier=1
        else:
            self.pipe_multiplier=-1
        self.angle=(math.atan(self.slope))
        print(self.angle)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        
        #---------IMAGE UNDISTORTION----------#
#        img = cv2.imread('test1.png')
#        h,w = img.shape[:2]
#        self.newcameramtx, self.roi=cv2.getOptimalNewCameraMatrix(self.mtx,self.dist,(w,h),1,(w,h))
#        dst = cv2.undistort(img, self.mtx, self.dist, None, self.newcameramtx)
#        cv2.imwrite('cal1.png',dst)
        #-------------------------------------#
        
        pixmap = QtGui.QPixmap("sample.png")
        painter.drawPixmap(10, 100,640,480, pixmap)
#        painter.drawPixmap(self,10, pixmap)
        pen = QtGui.QPen(QtCore.Qt.blue, 3)
        painter.setPen(pen)
        painter.drawLine(self.X2,self.Y2, self.new_X,self.new_Y)
        
#        pen2 = QtGui.QPen(QtCore.Qt.green, 3)
#        pen2.setStyle(QtCore.Qt.DashLine)
#        painter.setPen(pen2)
#        painter.drawLine(self.X_Coordinate, self.Y2, self.X_Coordinate, 100)
#        painter.drawLine(self.X_Coordinate, self.Y2, self.X_Coordinate, 400)
        #Change the coordinate to the one required

    def StoreValue1(self):
        self.Y1=self.y_cordinate
        self.X1=self.x_cordinate
        print("Value 1 Stored",self.X1,self.Y1) 
    def StoreValue2(self):
        self.Y2=self.y_cordinate
        self.X2=self.x_cordinate
        print("Value 2 Stored",self.X2,self.Y2)


def main():        
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()  
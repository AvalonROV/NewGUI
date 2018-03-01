import sys
import cv2
import numpy as np
#from PyQt4 import QtGui1, QtCore1, Qt1
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.Qt import *
    
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.resize(905, 700) # x=905, y=700
        self.centralwidget = QWidget(MainWindow)
        self.videoFrame1 = QLabel(self.centralwidget)
        self.videoFrame1.setGeometry(60, 30, 415, 300)
        self.videoFrame2 = QLabel(self.centralwidget)
        self.videoFrame2.setGeometry(480, 30, 415, 300) #videoframes end at y=330
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setGeometry(0, 0, 823, 21)
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)
        self.button = QPushButton('Quit', MainWindow)
        self.button.setGeometry(0, 0, 100, 30)
        self.button.clicked.connect(self.close_application)
        
        self.slider = QSlider(MainWindow)
        self.slider.setRange(0, 6)
        self.slider.setValue(0)
        self.slider.setGeometry(10, 130, 40, 200)        
    
        self.indicator1 = QLabel('inflate lifting bag', MainWindow)
        self.indicator1.setGeometry(20, 430, 100, 30)
        self.indicator2 = QLabel('detatch lifting bag', MainWindow)
        self.indicator2.setGeometry(150, 430, 100, 30)
        self.indicator3 = QLabel('drop power circuit', MainWindow)
        self.indicator3.setGeometry(280, 430, 100, 30)
        self.indicator4 = QLabel('depth reading', MainWindow)
        self.indicator4.setGeometry(540, 430, 100, 30)
        
        #OBS IMU display will be a graph, probably just x-y axes information
        #how to plot a graph?
        
    def close_application(self):
        print("Closing")
        sys.exit()
        
class Video():
    def __init__(self,capture):
        self.capture = capture
        self.currentFrame=np.array([])
 
    def captureNextFrame(self):
        """                           
        capture frame and reverse RBG BGR and return opencv image                                      
        """
        ret, readFrame=self.capture.read()
        if(ret==True):
            self.currentFrame=cv2.cvtColor(readFrame,cv2.COLOR_BGR2RGB)
 
    def convertFrame(self):
        """     converts frame to format suitable for             """
        try:
            height,width=self.currentFrame.shape[:2]
            img=QImage(self.currentFrame,
                              width,
                              height,
                              QImage.Format_RGB888)
            img=QPixmap.fromImage(img)
            self.previousFrame = self.currentFrame
            return img
        except:
            return None
            
 
class Gui(QMainWindow):
    def __init__(self,parent=None):
        QWidget.__init__(self,parent)
        self.ui = Ui_MainWindow()   #an object of class Ui_MainWindow
        self.ui.setupUi(self)       
        self.video1 = Video(cv2.VideoCapture(0))        #an object of class Video(argument)
        self.video2 = Video(cv2.VideoCapture(0))        #edit integer to change feed source
        self._timer = QTimer(self)
        self._timer.timeout.connect(self.play1)
        self._timer.timeout.connect(self.play2)
        self._timer.start(27)
        self.update()
 
    def play1(self):
        try:
            self.video1.captureNextFrame()
            self.ui.videoFrame1.setPixmap(
                self.video1.convertFrame())
            self.ui.videoFrame1.setScaledContents(True)
        except TypeError:
            print("No frame")
            
    def play2(self):
        try:
            self.video2.captureNextFrame()
            self.ui.videoFrame2.setPixmap(
                self.video2.convertFrame())
            self.ui.videoFrame2.setScaledContents(True)
        except TypeError:
            print("No frame")
 
def main():
    app = QApplication(sys.argv)
    ex = Gui()
    ex.show()
    sys.exit(app.exec_())
 
if __name__ == '__main__':
    main()
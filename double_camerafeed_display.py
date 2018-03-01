import sys
import cv2
import numpy as np
from PyQt4 import QtGui, QtCore, Qt
    
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.resize(923, 602)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.videoFrame1 = QtGui.QLabel(self.centralwidget)
        self.videoFrame1.setGeometry(QtCore.QRect(40, 32, 415, 300))
        self.videoFrame2 = QtGui.QLabel(self.centralwidget)
        self.videoFrame2.setGeometry(QtCore.QRect(460, 32, 415, 300))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 823, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)
        self.button = QtGui.QPushButton('Quit', MainWindow)
        self.button.setGeometry(QtCore.QRect(0, 0, 100, 30))
        self.button.clicked.connect(self.close_application)
        
        self.slider = QtGui.QSlider(MainWindow)
        self.slider.setRange(0, 3)
        self.slider.setValue(0)
        self.slider.setGeometry(QtCore.QRect( 0, 250, 40, 100))        
        
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
        """     converts frame to format suitable for QtGui            """
        try:
            height,width=self.currentFrame.shape[:2]
            img=QtGui.QImage(self.currentFrame,
                              width,
                              height,
                              QtGui.QImage.Format_RGB888)
            img=QtGui.QPixmap.fromImage(img)
            self.previousFrame = self.currentFrame
            return img
        except:
            return None
            
 
class Gui(QtGui.QMainWindow):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.video1 = Video(cv2.VideoCapture(0))
        self.video2 = Video(cv2.VideoCapture(0))
        self._timer = QtCore.QTimer(self)
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
    app = QtGui.QApplication(sys.argv)
    ex = Gui()
    ex.show()
    sys.exit(app.exec_())
 
if __name__ == '__main__':
    main()

from PyQt4.QtCore import *
from PyQt4.QtGui import *
#from PyQt4 import *
import sys

'''
aim of this script:
creating a class CircleWidget which can be used with a numerical parameter/argument to show a widget  
format is "icon = CircleWidget(self, integer 0 or 1, x-coord, y-coord)"
then can set the widget in a place of choice by varying x-coord and y-coord values

to do:
figure out how to create a central widget and add the CircleWidget to this 
'''

class CircleWidget(QWidget):
    def __init__(self, parent, aNumber, theX, theY):
        QWidget.__init__(self, parent)      #getting rid of parent here and line above, and self in 'icon=' does work
        self.number = aNumber
        self.xVal = theX
        self.yVal = theY
        
    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing) #makes nicer circles
        radx = 10; rady = 10
        center = QPoint(self.xVal, self.yVal)
        # draw red circle
        if (self.number == 0):
            p.setPen(Qt.red)
            #center = QPoint(self.xVal, self.yVal)
            p.setBrush(Qt.darkRed)  #set fill colour
            p.drawEllipse(center, radx, rady)
        else:
            p.setPen(Qt.green)
            #center = QPoint(self.xVal, self.yVal)        
            p.setBrush(Qt.darkGreen)
            p.drawEllipse(center, radx, rady)        

class MyMainWindow(QMainWindow):

    def __init__(self, parent):
        QMainWindow.__init__(self, parent)

        # Add content
        icon = CircleWidget(self, 0, 100, 50)     #2nd argument =aNumber, 3rd is the x-coordinate, 4th is the y-coordinate 
        #icon.show()
        self.setCentralWidget(icon)
        #button = QPushButton('button', icon)
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    sw = MyMainWindow(None)
    sw.show()
    app.exec_()
    sys.exit()
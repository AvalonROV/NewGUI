
from PyQt4.QtCore import *
from PyQt4.QtGui import *
#from PyQt4 import *
import sys

# As always, Qt allows us to subclass objects to override behaviour and generally monkey around
# with them how we want. This is the exact way that custom widget painting operates:
# you subclass the widget that you want as your base, and override paintEvent() to do your own painting.

'''
aim of this script:
creating a class CustomWidget which can be used with a numerical parameter/argument to show a widget  
format is "central = CustomWidget(self, 0)"
then can set the widget in a place of choice (hopefully)
will perhaps need to find some way of setting the widget in a location?

'''

class CustomWidget(QWidget):
    
    def __init__(self, parent, anumber):
        QWidget.__init__(self, parent)
        
        self._number = anumber
        
    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing) #makes nicer circles
        radx = 10; rady = 10
        # draw red circle
        if (self._number == 0):
            p.setPen(Qt.red)
            center = QPoint(100, 50)
            p.setBrush(Qt.darkRed)  #set fill colour
            p.drawEllipse(center, radx, rady)
        else:
            p.setPen(Qt.green)
            center2 = QPoint(100, 50)        
            p.setBrush(Qt.darkGreen)
            p.drawEllipse(center2, radx, rady)        

class MyMainWindow(QMainWindow):
    def __init__(self, parent):
        QMainWindow.__init__(self, parent)

        # Add content
        central = CustomWidget(self, 0)
        self.setCentralWidget(central)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    sw = MyMainWindow(None)
    sw.show()
    app.exec_()
    sys.exit()
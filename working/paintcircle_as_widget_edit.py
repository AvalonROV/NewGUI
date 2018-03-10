
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

COLOUR_RED = Qt.red
COLOUR_BLUE = Qt.blue
"""
class CircleWidget(QWidget):
    def __init__(self, parent, Number1, X1, Y1, Number2, X2, Y2):
        QWidget.__init__(self, parent)      #getting rid of parent here and line above, and self in 'icon=' does work
        self.number1 = Number1
        self.xVal1 = X1
        self.yVal1 = Y1
        self.number2 = Number2
        self.xVal2 = X2
        self.yVal2 = Y2
        
    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing) #makes nicer circles
        radx = 10; rady = 10
        center1 = QPoint(self.xVal1, self.yVal1)
        # draw red circle
        if (self.number1 == 0):
            p.setPen(Qt.red)
            #center = QPoint(self.xVal1, self.yVal1)
            p.setBrush(Qt.darkRed)  #set fill colour
            p.drawEllipse(center1, radx, rady)
        else:
            p.setPen(Qt.green)
            #center = QPoint(self.xVal, self.yVal)        
            p.setBrush(Qt.darkGreen)
            p.drawEllipse(center1, radx, rady)    
            
            center2 = QPoint(self.xVal2, self.yVal2)
            # draw red circle
            if (self.number2 == 0):
                p.setPen(Qt.red)
                #center = QPoint(self.xVal1, self.yVal1)
                p.setBrush(Qt.darkRed)  #set fill colour
                p.drawEllipse(center2, radx, rady)
            else:
                p.setPen(Qt.green)
                #center = QPoint(self.xVal, self.yVal)        
                p.setBrush(Qt.darkGreen)
                p.drawEllipse(center2, radx, rady)
""" 
class paint_thing(QWidget):
    def __init__(self, object_list):
        super(paint_thing, self).__init__()
        self.object_list = object_list
        
    def paintEvent(self):
        self.painter = QPainter(self)
        self.painter.setRenderHint(QPainter.Antialiasing)
        for paint_object in self.object_list:
            paint_object.draw_circle(self.painter)

class paint_circle():
    def __init__(self, x_center, y_center, rad_x, rad_y, colour):
        self.x_center = x_center
        self.y_center = y_center
        self.rad_x = rad_x
        self.rad_y = rad_y
        self.colour = colour
        self.center = QPoint(self.x_center, self.y_center)
    
    def draw_circle(self, painter):
        painter.setPen(self.colour)
        painter.setBrush(self.colour)
        painter.drawEllipse(self.center, self.rad_x, self.rad_y)        

class MyMainWindow(QMainWindow):

    def __init__(self, parent):
        QMainWindow.__init__(self, parent)

        # Add content
        #icon = CircleWidget(self, 1, 100, 50, 0, 120, 50)     #2nd argument =aNumber, 3rd is the x-coordinate, 4th is the y-coordinate 
        #icon.show()
        circle1 = paint_circle(100, 50, 10, 10, COLOUR_BLUE)
        circle2 = paint_circle(200, 50, 10, 10, COLOUR_RED)
        object_list = [circle1, circle2]        
        paint_thingy = paint_thing(object_list)
        
        
        
        paint_thingy.paintEvent()
        
        self.mainLayout = QHBoxLayout()
        self.mainLayout.addWidget(paint_thingy)
        
        
        # central widget
        self.centralWidget = QWidget()
        self.centralWidget.setLayout(self.mainLayout)
    
        # set central widget
        self.setCentralWidget(self.centralWidget)
        
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    sw = MyMainWindow(None)
    sw.show()
    app.exec_()
    sys.exit()
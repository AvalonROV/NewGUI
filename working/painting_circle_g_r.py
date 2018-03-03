from PyQt4.QtCore import *
from PyQt4.QtGui import *

class DrawCircles(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        # setGeometry(x_pos, y_pos, width, height)
        self.setGeometry(300, 300, 350, 350)
        self.setWindowTitle('Draw circles')

#beginning of painting
    def paintEvent(self, event):
        paint = QPainter()
        paint.begin(self)
        paint.setRenderHint(QPainter.Antialiasing) #makes nicer circles
        radx = 10
        rady = 10
        # draw red circles
        paint.setPen(Qt.red)
        center = QPoint(100, 100)
        paint.setBrush(Qt.darkRed)  #set fill colour
        paint.drawEllipse(center, radx, rady)
        #beginning of green circle
        paint.setPen(Qt.green)
        center2 = QPoint(150, 100)        
        paint.setBrush(Qt.darkGreen)
        paint.drawEllipse(center2, radx, rady)        
        paint.end()            

app = QApplication([])
circles = DrawCircles()
circles.show()
app.exec_()
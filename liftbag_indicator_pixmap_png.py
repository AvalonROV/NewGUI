import os
import sys
from PyQt4.QtGui import *

# Create window
app = QApplication(sys.argv)
w = QWidget()
w.setWindowTitle("Displaying Indicator") 
w.setGeometry(50, 50, 600, 300)
# Create widget, place in location (10,10)
ind1 = QLabel(w)
ind2 = QLabel(w)

ind1.move(85, 160)
ind2.move(235, 160)
inflate = QPushButton("Inflate",w)
detatch = QPushButton("Detatch",w)
inflate.move(50, 200)
detatch.move(200, 200)
print(inflate.size())

picfile1 = 'green.png'
picfile2 = 'red.png'
loc_g = os.getcwd() + '\\' + picfile1
loc_r = os.getcwd() + '\\' + picfile2
print(loc_g), print(loc_r)

if os.path.isfile(loc_g):
    pixmap_g = QPixmap(loc_g)
    pixmap_r = QPixmap(loc_r)
    pixmap_g = pixmap_g.scaledToWidth(10)   #scale to width of 10
    pixmap_r = pixmap_r.scaledToWidth(10)
    #print(pixmap_g.size())
    ind1.setPixmap(pixmap_g)    
    ind2.setPixmap(pixmap_g)

    # Draw window
    w.show()
    app.exec_()
else:
    print("I expected to find a png picture called green.png in "+ os.getcwd())
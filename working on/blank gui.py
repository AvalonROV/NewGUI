#!/usr/bin/python
# -*- coding: utf-8 -*-

import cv2
import sys
import numpy as np
import matplotlib as mpl
from PyQt4.QtGui import*
from PyQt4.QtCore import *


app = QApplication(sys.argv) # Creat a new QApplication object. This manages
                                # the GUI application's control flow and main
                                # settings.

#will get x and y axis sizemometer information from the wifi connection
#either plot x and y axis data against each other

#also display the x and y OBS data for levelling the device

class Gui(QWidget):
#base class of all user interface objects. 

    def __init__(self):
        super(Gui, self).__init__()
        self.initUI()

    def initUI(self):

        title1_font = QFont("Arial", 16, QFont.Bold)    #Define title1 font

        # Title
        application_title = QLabel()                        #Create label for the window title
        application_title.setText("ROV Control Interface")  #Set Text
        application_title.setFont(title1_font)              #Set font
        application_title.setAlignment(Qt.AlignCenter)      #Set Allignment
        #self.quit_button = QPushButton('Quit')
        #self.quit_button.clicked.connect(self.close_app)

        grid = QGridLayout()              #Create layout container
        #grid.addWidget(self.quit_button, 10, 1)
        grid.addWidget(application_title, 0, 0)
        self.setLayout(grid)    #Set the layout

        self.setGeometry(10, 100, 600, 300)
        self.setWindowTitle('Test')    
        self.show()

    #def close_app(self):
        #print("Closing")
        #sys.exit()

def main():

    ex = Gui()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

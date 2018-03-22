#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import numpy as np
# matplotlib imports
import matplotlib
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import random
# end of matplotlib imports

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

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.button = QPushButton('Plot')
        self.button.clicked.connect(self.plot)
        
        
        
        # create layout container
        grid = QGridLayout()              
        #grid.addWidget(the_widget, row_int, col_int)
        grid.addWidget(self.canvas, 0, 0)
        grid.addWidget(self.button, 1, 0)        
        self.setLayout(grid)    #Set the layout

        self.setGeometry(10, 100, 600, 500)
        self.setWindowTitle('Seisemometer Graph')    
        self.show()


    def plot(self):
        #plot some random stuff 

        # create an axis
        ax = self.figure.add_subplot(111)
        
        # discards the old graph
        ax.clear()
        
        ax.grid(which='both', linestyle='-')
        ax.set_xlabel('Time')
        ax.set_ylabel('Amplitude')        
        ax.set_xticks([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14])
        # plot data
        #data = [random.random() for i in range(14)]
        #ax.plot(data, '*-') 
        #OR:
        ax.plot([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14], [random.random() for i in range(14)], 'x-')
        
        '''
    here we will get the data from the C++ wrapper by importing it as a library/module and using 
    a method from said library/module to get the sizemometer data.
        '''
        
        # refresh canvas to actually display the graph
        self.canvas.draw()



def main():

    ex = Gui()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

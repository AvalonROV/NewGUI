#https://stackoverflow.com/questions/12459811/how-to-embed-matplotlib-in-pyqt-for-dummies

from PyQt4 import QtGui
import sys
# matplotlib imports
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import random
# end of matplotlib imports
import numpy as np

class Window(QtGui.QDialog):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        # set a figure instance to plot on
        self.figure = Figure()

        # Canvas Widget that displays the `figure`
        # takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # Navigation widget which is unnecessary
        # takes the Canvas widget and a parent
        #self.toolbar = NavigationToolbar(self.canvas, self)

        # button connected to `plot` method
        self.button = QtGui.QPushButton('Plot')
        self.button.clicked.connect(self.plot)

        # set vertical box layout
        layout = QtGui.QVBoxLayout()
        #layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addWidget(self.button)
        self.setLayout(layout)
        
        '''
        ax = self.figure.add_subplot(111)
        ax.clear()    
        ax.plot([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14], [random.random() for i in range(14)], 'x-')
        self.canvas.draw()
        '''
        
    def plot(self):
        #plot some random stuff 

        # create an axis
        ax = self.figure.add_subplot(111)

        # discards the old graph
        ax.clear()

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
        
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)

    main = Window()
    main.show()

    sys.exit(app.exec_())
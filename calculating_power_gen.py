#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import numpy as np
import math
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

        CalcBtn = QPushButton('Calculate')
        CalcBtn.clicked.connect(self.calculate)
        Quit = QPushButton('Quit')
        Quit.clicked.connect(QCoreApplication.instance().quit)
        
        blank = QLabel('')
        warning = QLabel('DO NOT USE ANY OF THE ARROWS IN THE CABLE AREA')
        #power_lbl = QLabel('Power (W)')   #probs not needed
        num_tb_lbl = QLabel('Number of Turbines')
        density_lbl = QLabel('Density of Seawater (kg/m^3')
        diameter_lbl = QLabel('Diameter of One Rotor (m)')
        water_vel_lbl = QLabel('Velocity of Water (knots)')
        efficiency_lbl = QLabel('Efficiency of Turbines (%)')
        ans_lbl = QLabel('Answer - Maximum Power Generated (W)')
        
        
        #self.power = QDoubleSpinBox()
        self.num_tb = QDoubleSpinBox(); self.num_tb.setRange(0, 30)
        self.density = QDoubleSpinBox(); self.density.setDecimals(3); self.density.setValue(1.025)
        self.diameter = QDoubleSpinBox(); self.diameter.setRange(0, 50)
        self.water_vel = QDoubleSpinBox(); self.water_vel.setRange(0, 20)
        self.efficiency = QDoubleSpinBox(); self.efficiency.setRange(0, 100)
        self.ans = QDoubleSpinBox(); self.ans.setRange(0, 20000)
        

        grid = QGridLayout()              #Create layout container
        #grid.addWidget(self.quit_button, 10, 1)
        #grid.addWidget(warning, 0, 1)
        grid.addWidget(num_tb_lbl, 1, 1)
        grid.addWidget(density_lbl, 2, 1)
        grid.addWidget(diameter_lbl, 3, 1)
        grid.addWidget(water_vel_lbl, 4, 1)
        grid.addWidget(efficiency_lbl, 5, 1)
        grid.addWidget(blank, 6, 1, 1, 1)
        grid.addWidget(ans_lbl, 7, 1)
        grid.addWidget(self.num_tb, 1, 2)
        grid.addWidget(self.density, 2, 2)
        grid.addWidget(self.diameter, 3, 2)
        grid.addWidget(self.water_vel, 4, 2)
        grid.addWidget(self.efficiency, 5, 2)
        grid.addWidget(CalcBtn, 6, 2)
        grid.addWidget(self.ans, 7, 2)
        self.setLayout(grid)    #Set the layout
        grid.setSpacing(20)
        self.setGeometry(10, 100, 600, 260)
        self.setWindowTitle('Calculating Power Generated')    
        self.show()

    def calculate(self):
        #NEED TO CONVERT KNOTS TO M/S
        N = self.num_tb.value()
        p = self.density.value()
        d = self.diameter.value()
        a = (d/2)**2 * math.pi
        V = self.water_vel.value()  #either 463/900 or 33/64
        Cp = self.efficiency.value()
        pwr= N/2 * p * a * (V*463/900)**3 * Cp/100
        self.ans.setValue(pwr)

    #def close_app(self):
        #print("Closing")
        #sys.exit()

def main():

    ex = Gui()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

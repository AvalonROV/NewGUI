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

class Gui(QWidget):
#base class of all user interface objects. 

    def __init__(self):
        super(Gui, self).__init__()
        self.initUI()

    def initUI(self):

        calc_btn = QPushButton('Calculate')
        calc_btn.clicked.connect(self.calculate)
        quit = QPushButton('Quit')
        quit.clicked.connect(QCoreApplication.instance().quit)
    
        blank = QLabel('')
        tol_lbl = QLabel('Take-off Location')
        heading_lbl = QLabel('Heading (degrees)')
        asc_as_lbl = QLabel('Ascent Airspeed (m/s)')
        asc_rate_lbl = QLabel('Ascent Rate (m/s)')
        eng_fail_time_lbl = QLabel('Time of Engine Failure (s)')
        desc_as_lbl = QLabel('Descent Airspeed (m/s)')
        desc_rate_lbl = QLabel('Descent Rate (m/s)')
        w_spd_lbl = QLabel('Wind Speed (m/s)')
        w_direc_lbl = QLabel('Wind Blowing From (degrees)')
        asc_dist_x_lbl = QLabel('Ascent Distance X (m)')
        asc_dist_y_lbl = QLabel('Ascent Distance Y (m)')
        desc_dist_x_lbl = QLabel('Descent Distance X (m)')
        desc_dist_y_lbl = QLabel('Descent Distance Y (m)')        
        wind_dist_x_lbl = QLabel('Wind Distance X (m)')
        wind_dist_y_lbl = QLabel('Wind Distance Y (m)')
        total_dist_x_lbl = QLabel('Total Distance X (m)')
        total_dist_y_lbl = QLabel('Total Distance Y (m)')        
        ans_distance_lbl = QLabel('Location: Distance (m)')
        ans_angle_lbl = QLabel('Location: Direction (degrees)') # zero degrees is east , 90 degrees is north
        ans_heading_lbl = QLabel('Location: Heading (degrees)') # zero degrees is north, 90 degrees is east

        self.tol = QDoubleSpinBox()
        self.heading = QDoubleSpinBox()
        self.heading.setRange(0, 360)
        self.asc_as = QDoubleSpinBox()
        self.asc_rate = QDoubleSpinBox()
        self.eng_fail_time = QDoubleSpinBox()
        self.eng_fail_time.setRange(0, 1000)
        self.desc_as = QDoubleSpinBox()
        self.desc_rate = QDoubleSpinBox()
        self.w_spd = QDoubleSpinBox()
        self.w_dir = QDoubleSpinBox(); self.w_dir.setRange(0, 360)
        self.asc_dist_x = QDoubleSpinBox(); self.asc_dist_x.setRange(-10000, 10000)
        self.asc_dist_y = QDoubleSpinBox(); self.asc_dist_y.setRange(-10000, 10000)
        self.desc_dist_x = QDoubleSpinBox(); self.desc_dist_x.setRange(-10000, 10000)
        self.desc_dist_y = QDoubleSpinBox(); self.desc_dist_y.setRange(-10000, 10000)
        self.wind_dist_x = QDoubleSpinBox(); self.wind_dist_x.setRange(-10000, 10000)
        self.wind_dist_y = QDoubleSpinBox(); self.wind_dist_y.setRange(-10000, 10000)
        self.total_dist_x = QDoubleSpinBox(); self.total_dist_x.setRange(-10000, 10000)
        self.total_dist_y = QDoubleSpinBox(); self.total_dist_y.setRange(-10000, 10000)
        self.ans_dist = QDoubleSpinBox(); self.ans_dist.setRange(-10000, 10000)
        self.ans_angle = QDoubleSpinBox(); self.ans_angle.setRange(-360, 360)
        self.ans_heading = QDoubleSpinBox(); self.ans_heading.setRange(-360, 360)

        grid = QGridLayout()
        #grid.setSpacing(10)

        grid.addWidget(heading_lbl, 2, 0)
        grid.addWidget(self.heading, 2, 1)
        grid.addWidget(asc_as_lbl, 3, 0)
        grid.addWidget(self.asc_as, 3, 1)
        grid.addWidget(asc_rate_lbl, 4, 0)
        grid.addWidget(self.asc_rate, 4, 1)
        grid.addWidget(eng_fail_time_lbl, 5, 0)
        grid.addWidget(self.eng_fail_time, 5, 1)
        grid.addWidget(desc_as_lbl, 6, 0)
        grid.addWidget(self.desc_as, 6, 1)
        grid.addWidget(desc_rate_lbl, 7, 0)
        grid.addWidget(self.desc_rate, 7, 1)
        #grid.addWidget(w_spd_lbl, 8, 0)
        #grid.addWidget(self.w_spd, 8, 1)
        grid.addWidget(w_direc_lbl, 9, 0)
        grid.addWidget(self.w_dir, 9, 1)
        grid.addWidget(calc_btn, 10, 1)
        grid.addWidget(blank, 11, 0)
        grid.addWidget(asc_dist_x_lbl, 12, 0)        
        grid.addWidget(self.asc_dist_x, 12, 1)
        grid.addWidget(asc_dist_y_lbl, 12, 2)
        grid.addWidget(self.asc_dist_y, 12, 3)        
        grid.addWidget(desc_dist_x_lbl, 13, 0)
        grid.addWidget(self.desc_dist_x, 13, 1)
        grid.addWidget(desc_dist_y_lbl, 13, 2)
        grid.addWidget(self.desc_dist_y, 13, 3)
        grid.addWidget(wind_dist_x_lbl, 14, 0)
        grid.addWidget(self.wind_dist_x, 14, 1)
        grid.addWidget(wind_dist_y_lbl, 14, 2)
        grid.addWidget(self.wind_dist_y, 14, 3)
        grid.addWidget(total_dist_x_lbl, 15, 0)
        grid.addWidget(self.total_dist_x, 15, 1)
        grid.addWidget(total_dist_y_lbl, 15, 2)        
        grid.addWidget(self.total_dist_y, 15, 3)        
        grid.addWidget(blank, 16, 0)
        grid.addWidget(ans_distance_lbl, 17, 0)
        grid.addWidget(self.ans_dist, 17, 1)
        grid.addWidget(ans_angle_lbl, 18, 0)
        grid.addWidget(self.ans_angle, 18, 1)
        grid.addWidget(ans_heading_lbl, 19, 0)
        grid.addWidget(self.ans_heading, 19, 1)
        grid.addWidget(quit, 20, 3)

        self.setLayout(grid)    #Set the layout

        self.setGeometry(10, 100, 600, 300)
        self.setWindowTitle('Calculating Location of Aicraft Wreckage')
        self.show()

    def calculate(self):
        at = self.eng_fail_time.value()
        h = 90 - self.heading.value()   #convert heading-->cartesian   
        hrad = ((h/180)*math.pi)        #convert rad-->deg
        aas = self.asc_as.value()        
        ar = self.asc_rate.value()
        das = self.desc_as.value()
        dr = self.desc_rate.value()
        wd = 270 - self.w_dir.value()   #convert wind origin-->cartesian
        wdrad = ((wd/180)*math.pi)      #convert rad-->deg 
        height = (at*ar)                #height reached
        dt = (height/dr)                #descent time
        ax = (at*aas*math.cos(hrad))
        ay = (at*aas*math.sin(hrad))
        dx = (dt*das*math.cos(hrad))
        dy = (dt*das*math.sin(hrad))
        wd = -(-1/720)*dt**3 +25*dt
        '''
        for wd equation, integrate equation given, then integrate expression 
        between limits of time of engine failure (at) and total overall time (at+dt)
        '''     
        wx = (wd*math.cos(wdrad))
        wy = (wd*math.sin(wdrad))
        totalx = (ax + dx + wx)
        totaly = (ay + dy + wy)
        dist = (math.sqrt(totalx**2 +totaly**2))
        
        if totaly>=0 and totalx>0:
            angle = ((math.atan(totaly/totalx))*180/math.pi)
        elif totaly<=0 and totalx>0:
            angle = ((math.atan(totaly/totalx))*180/math.pi)
        elif totaly>=0 and totalx<0:
            angle = ((math.atan(totaly/totalx))*180/math.pi +180)
        elif totaly<=0 and totalx<0:
            angle = ((math.atan(totaly/totalx))*180/math.pi + 180)
        elif totaly==0 and totalx==0:
            angle = 0
        elif totaly<0 and totalx==0:
            angle = 270
        elif totaly>0 and totalx==0:
            angle = 90            
        
        self.asc_dist_x.setValue(ax)
        self.asc_dist_y.setValue(ay)
        self.desc_dist_x.setValue(dx)
        self.desc_dist_y.setValue(dy)
        self.wind_dist_x.setValue(wx)
        self.wind_dist_y.setValue(wy)
        self.total_dist_x.setValue(totalx)
        self.total_dist_y.setValue(totaly)
        self.ans_dist.setValue(dist)
        self.ans_angle.setValue(angle)
        self.ans_heading.setValue(90 - angle)
        

    #def close_app(self):
        #print("Closing")
        #sys.exit()

def main():

    ex = Gui()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

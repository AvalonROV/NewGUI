#obs graph, imu reading, depth, power generation calculation
#ADD LINEEDIT TO INPUT THE EXPRESSION TO BE INTEGRATED

import sys
import numpy as np
import math
from scipy.integrate import quad
# matplotlib imports
import matplotlib
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import random
# end of matplotlib imports
from PyQt4.QtGui import*
from PyQt4.QtCore import *

app = QApplication(sys.argv)

class Gui(QWidget):
   #base class of all user interface objects. 

    def __init__(self):
        super(Gui, self).__init__()
        self.initUI()

    def initUI(self):
        
               
        graph_task = QLabel('Displaying Sizemometer Graph');
        graph_task.setStyleSheet(" font: bold; qproperty-alignment: AlignCenter")
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.button = QPushButton('Plot')
        self.button.clicked.connect(self.plot)
        
        power_task = QLabel('Calculating Max Power Generated')
        power_task.setStyleSheet(" font: bold; qproperty-alignment: AlignCenter")
        power_url_lbl = QLabel('DeepZoom Link:') 
        power_url = QLineEdit('http://www.deepzoom.com/')
        p_calc_btn = QPushButton('Calculate Power')
        p_calc_btn.clicked.connect(self.calculate_p)
        blank = QLabel('')
        warning = QLabel('DO NOT USE ANY OF THE ARROWS IN THE CABLE AREA')
        num_tb_lbl = QLabel('Number of Turbines')
        density_lbl = QLabel('Density of Seawater (kg/m^3')
        diameter_lbl = QLabel('Diameter of One Rotor (m)')
        water_vel_lbl = QLabel('Velocity of Water (knots)')
        efficiency_lbl = QLabel('Efficiency of Turbines (%)')
        ans_lbl = QLabel('Answer - Maximum Power Generated (W)')
        self.num_tb = QDoubleSpinBox(); self.num_tb.setRange(0, 30)
        self.density = QDoubleSpinBox(); self.density.setDecimals(3); self.density.setValue(1.025)
        self.diameter = QDoubleSpinBox(); self.diameter.setRange(0, 50)
        self.water_vel = QDoubleSpinBox(); self.water_vel.setRange(0, 20)
        self.efficiency = QDoubleSpinBox(); self.efficiency.setRange(0, 100)
        self.p_ans = QDoubleSpinBox(); self.p_ans.setRange(0, 20000)        
        
        #display IMU and depth reading
        readings_task = QLabel('Readings - IMU and Depth')
        readings_task.setStyleSheet(" font: bold; qproperty-alignment: AlignCenter") 
        imu_x_lbl = QLabel('IMU x Value:')
        imu_y_lbl = QLabel('IMU y Value:')
        self.imu_x = QLineEdit()
        self.imu_y = QLineEdit()
        depth_lbl = QLabel('Depth Reading:')
        self.depth = QLineEdit()
        
        #display gui for calculating location of a/c wreckage
        location_task = QLabel('Calculating Location of Wreckage')
        location_task.setStyleSheet(" font: bold; qproperty-alignment: AlignCenter")
        calc_btn_loc = QPushButton('Calculate Location')
        calc_btn_loc.clicked.connect(self.calculate_loc)
        tol_lbl = QLabel('Take-off Location')
        heading_lbl = QLabel('Heading (degrees)')
        asc_as_lbl = QLabel('Ascent Airspeed (m/s)')
        asc_rate_lbl = QLabel('Ascent Rate (m/s)')
        eng_fail_time_lbl = QLabel('Time of Engine Failure (s)')
        desc_as_lbl = QLabel('Descent Airspeed (m/s)')
        desc_rate_lbl = QLabel('Descent Rate (m/s)')
        w_direc_lbl = QLabel('Wind Blowing From (degrees)')
        w_eqn_lbl = QLabel('Wind Direction Equation')
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
        self.heading = QDoubleSpinBox(); self.heading.setRange(0, 360)
        self.asc_as = QDoubleSpinBox()
        self.asc_rate = QDoubleSpinBox()
        self.eng_fail_time = QDoubleSpinBox(); self.eng_fail_time.setRange(0, 1000)
        self.desc_as = QDoubleSpinBox()
        self.desc_rate = QDoubleSpinBox()
        self.w_dir = QDoubleSpinBox(); self.w_dir.setRange(0, 360)
        self.w_eqn = QLineEdit(); self.w_eqn.setText('-(t/720)**2 + 25')
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
        
        # create graph layout container    
        graph = QVBoxLayout()
        graph.addWidget(graph_task)
        graph.addWidget(self.canvas)
        graph.addWidget(self.button)        
        
        # create centre layout container        
        p_calc = QGridLayout()
        p_calc.addWidget(power_task, 0, 1, 1, 2)
        p_calc.addWidget(num_tb_lbl, 1, 1); p_calc.addWidget(self.num_tb, 1, 2)
        p_calc.addWidget(density_lbl, 2, 1); p_calc.addWidget(self.density, 2, 2)
        p_calc.addWidget(diameter_lbl, 3, 1); p_calc.addWidget(self.diameter, 3, 2)
        p_calc.addWidget(water_vel_lbl, 4, 1); p_calc.addWidget(self.water_vel, 4, 2)
        p_calc.addWidget(efficiency_lbl, 5, 1); p_calc.addWidget(self.efficiency, 5, 2)
        p_calc.addWidget(p_calc_btn, 6, 1, 1, 2)
        #p_calc.addWidget(blank, 6, 1, 1, 1)
        p_calc.addWidget(ans_lbl, 8, 1); p_calc.addWidget(self.p_ans, 8, 2)
        p_calc.addWidget(blank, 7, 1)
        p_calc.addWidget(power_url_lbl, 9, 1); p_calc.addWidget(power_url, 10, 1, 1, 2)
        p_calc.addWidget(blank, 11, 1)
        p_calc.addWidget(readings_task, 12, 1, 1, 2)
        p_calc.addWidget(imu_x_lbl, 13, 1); p_calc.addWidget(self.imu_x, 13, 2)
        p_calc.addWidget(imu_y_lbl, 14, 1); p_calc.addWidget(self.imu_y, 14, 2)
        p_calc.addWidget(blank, 15, 1)
        p_calc.addWidget(depth_lbl, 16, 1); p_calc.addWidget(self.depth, 16, 2)
        p_calc.addWidget(blank, 17, 3)
        
        # create calculating location layout container        
        loc_calc = QGridLayout()
        loc_calc.addWidget(location_task, 0, 0, 1, 4)
        loc_calc.addWidget(heading_lbl, 2, 0)
        loc_calc.addWidget(self.heading, 2, 1)
        loc_calc.addWidget(asc_as_lbl, 3, 0)
        loc_calc.addWidget(self.asc_as, 3, 1)
        loc_calc.addWidget(asc_rate_lbl, 4, 0)
        loc_calc.addWidget(self.asc_rate, 4, 1)
        loc_calc.addWidget(eng_fail_time_lbl, 5, 0)
        loc_calc.addWidget(self.eng_fail_time, 5, 1)
        loc_calc.addWidget(desc_as_lbl, 6, 0); loc_calc.addWidget(self.desc_as, 6, 1)
        loc_calc.addWidget(desc_rate_lbl, 7, 0); loc_calc.addWidget(self.desc_rate, 7, 1)
        loc_calc.addWidget(w_eqn_lbl, 8, 0); loc_calc.addWidget(self.w_eqn, 8, 1, 1, 2)
        loc_calc.addWidget(w_direc_lbl, 9, 0); loc_calc.addWidget(self.w_dir, 9, 1)
        loc_calc.addWidget(calc_btn_loc, 10, 0, 1, 4)
        loc_calc.addWidget(blank, 11, 0)
        loc_calc.addWidget(asc_dist_x_lbl, 12, 0); loc_calc.addWidget(self.asc_dist_x, 12, 1)
        loc_calc.addWidget(asc_dist_y_lbl, 12, 2); loc_calc.addWidget(self.asc_dist_y, 12, 3)        
        loc_calc.addWidget(desc_dist_x_lbl, 13, 0); loc_calc.addWidget(self.desc_dist_x, 13, 1)
        loc_calc.addWidget(desc_dist_y_lbl, 13, 2); loc_calc.addWidget(self.desc_dist_y, 13, 3)
        loc_calc.addWidget(wind_dist_x_lbl, 14, 0); loc_calc.addWidget(self.wind_dist_x, 14, 1)
        loc_calc.addWidget(wind_dist_y_lbl, 14, 2); loc_calc.addWidget(self.wind_dist_y, 14, 3)
        loc_calc.addWidget(total_dist_x_lbl, 15, 0); loc_calc.addWidget(self.total_dist_x, 15, 1)
        loc_calc.addWidget(total_dist_y_lbl, 15, 2); loc_calc.addWidget(self.total_dist_y, 15, 3)        
        loc_calc.addWidget(blank, 16, 0)
        loc_calc.addWidget(ans_distance_lbl, 17, 0); loc_calc.addWidget(self.ans_dist, 17, 1)
        loc_calc.addWidget(ans_angle_lbl, 18, 0); loc_calc.addWidget(self.ans_angle, 18, 1)
        loc_calc.addWidget(ans_heading_lbl, 19, 0); loc_calc.addWidget(self.ans_heading, 19, 1)
        

        # create horizontal box layout container
        hbox = QHBoxLayout()
        hbox.addLayout(graph)
        hbox.addLayout(p_calc)
        hbox.addLayout(loc_calc)
        self.setLayout(hbox)    #Set the layout

        self.setGeometry(10, 100, 1200, 600)
        self.setWindowTitle('Co-pilot GUI')    
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

    def calculate_p(self):
        #NEED TO CONVERT KNOTS TO M/S
        N = self.num_tb.value()
        p = self.density.value()
        d = self.diameter.value()
        a = (d/2)**2 * math.pi
        V = self.water_vel.value()  #either 463/900 or 33/64
        Cp = self.efficiency.value()
        pwr= N/2 * p * a * (V*463/900)**3 * Cp/100
        self.p_ans.setValue(pwr)
        
    def calculate_loc(self):
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
        dt = (height/(dr))                #descent time
        eqn = str(self.w_eqn.text())
        ax = (at*aas*math.cos(hrad))
        ay = (at*aas*math.sin(hrad))
        dx = (dt*das*math.cos(hrad))
        dy = (dt*das*math.sin(hrad))   
        def integrand(t):
            return eval(eqn)
            #return -(t/720)**2 + 25
        wd, err = quad(integrand, at, at+dt)
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
    



def main():

    ex = Gui()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
 
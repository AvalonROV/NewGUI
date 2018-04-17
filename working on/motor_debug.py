import sys
import numpy as np
from PyQt4.QtGui import*
from PyQt4.QtCore import *
from time import sleep

app = QApplication(sys.argv) # Creat a new QApplication object. This manages
                                # the GUI application's control flow and main
                                # settings.

class Gui(QWidget):
#base class of all user interface objects. 

    def __init__(self):
        super(Gui, self).__init__()
        self.initUI()

    def initUI(self):
        
        #labels for name, spinnner for magnitude, spinner for changing order, lineedit for string output, button for switch
        
        name_lbl = QLabel('Name'); name_lbl.setStyleSheet(" font: bold; qproperty-alignment: AlignCenter")
        val_lbl = QLabel('Thrust value'); val_lbl.setStyleSheet(" font: bold; qproperty-alignment: AlignCenter")
        btn_lbl = QLabel('Flip direction?'); btn_lbl.setStyleSheet(" font: bold; qproperty-alignment: AlignCenter")
        fval_lbl = QLabel('Flip val (-1=y, 1=n)'); btn_lbl.setStyleSheet(" font: bold; qproperty-alignment: AlignCenter")
        order_lbl = QLabel('Order in string'); order_lbl.setStyleSheet(" font: bold; qproperty-alignment: AlignCenter")
        
        m1_lbl = QLabel('Forward Left Motor')
        m2_lbl = QLabel('Forward Right Motor')
        m3_lbl = QLabel('Back Left Motor')
        m4_lbl = QLabel('Back Right Motor')
        m5_lbl = QLabel('Front Motor')
        m6_lbl = QLabel('Back Motor')

        m1_mag = QSpinBox(); m1_mag.setRange(1100, 1900); m1_mag.setValue(1500)
        m2_mag = QSpinBox(); m2_mag.setRange(1100, 1900); m2_mag.setValue(1500)
        m3_mag = QSpinBox(); m3_mag.setRange(1100, 1900); m3_mag.setValue(1500)
        m4_mag = QSpinBox(); m4_mag.setRange(1100, 1900); m4_mag.setValue(1500)
        m5_mag = QSpinBox(); m5_mag.setRange(1100, 1900); m5_mag.setValue(1500)
        m6_mag = QSpinBox(); m6_mag.setRange(1100, 1900); m6_mag.setValue(1500)

        m1_btn = QPushButton('Flip Direction'); m1_btn.clicked.connect(self.flip)
        m2_btn = QPushButton('Flip Direction'); m2_btn.clicked.connect(self.flip)
        m3_btn = QPushButton('Flip Direction'); m3_btn.clicked.connect(self.flip)
        m4_btn = QPushButton('Flip Direction'); m4_btn.clicked.connect(self.flip)
        m5_btn = QPushButton('Flip Direction'); m5_btn.clicked.connect(self.flip)
        m6_btn = QPushButton('Flip Direction'); m6_btn.clicked.connect(self.flip)
        
        m1_val = QSpinBox(); m1_val.setValue(1); m1_val.setRange(-1, 1); m1_val.setSingleStep(2)
        m2_val = QSpinBox(); m2_val.setValue(1); m2_val.setRange(-1, 1); m2_val.setSingleStep(2)
        m3_val = QSpinBox(); m3_val.setValue(1); m3_val.setRange(-1, 1); m3_val.setSingleStep(2)
        m4_val = QSpinBox(); m4_val.setValue(1); m4_val.setRange(-1, 1); m4_val.setSingleStep(2)
        m5_val = QSpinBox(); m5_val.setValue(1); m5_val.setRange(-1, 1); m5_val.setSingleStep(2)
        m6_val = QSpinBox(); m6_val.setValue(1); m6_val.setRange(-1, 1); m6_val.setSingleStep(2)

        m1_num = QSpinBox(); m1_num.setRange(1, 6); m1_num.setValue(1)
        m2_num = QSpinBox(); m2_num.setRange(1, 6); m2_num.setValue(2)
        m3_num = QSpinBox(); m3_num.setRange(1, 6); m3_num.setValue(3)
        m4_num = QSpinBox(); m4_num.setRange(1, 6); m4_num.setValue(4)
        m5_num = QSpinBox(); m5_num.setRange(1, 6); m5_num.setValue(5)
        m6_num = QSpinBox(); m6_num.setRange(1, 6); m6_num.setValue(6)
        
        str_disp = QLineEdit('')
        str_disp_btn = QPushButton('Display String to Motor'); str_disp_btn.clicked.connect(self.stringedit)
        
        grid = QGridLayout()              #Create layout container
        
        grid.addWidget(name_lbl, 1, 1)
        grid.addWidget(val_lbl, 1, 2)
        grid.addWidget(btn_lbl, 1, 3)
        grid.addWidget(fval_lbl, 1, 4)
        grid.addWidget(order_lbl, 1, 5)
        
        grid.addWidget(m1_lbl, 2, 1)
        grid.addWidget(m1_mag, 2, 2)
        grid.addWidget(m1_btn, 2, 3)
        grid.addWidget(m1_val, 2, 4)
        grid.addWidget(m1_num, 2, 5)
        
        grid.addWidget(m2_lbl, 3, 1)
        grid.addWidget(m2_mag, 3, 2)
        grid.addWidget(m2_btn, 3, 3)
        grid.addWidget(m2_val, 3, 4)
        grid.addWidget(m2_num, 3, 5)
        
        grid.addWidget(m3_lbl, 4, 1)
        grid.addWidget(m3_mag, 4, 2)
        grid.addWidget(m3_btn, 4, 3)
        grid.addWidget(m3_val, 4, 4)
        grid.addWidget(m3_num, 4, 5)
        
        grid.addWidget(m4_lbl, 5, 1)
        grid.addWidget(m4_mag, 5, 2)
        grid.addWidget(m4_btn, 5, 3)
        grid.addWidget(m4_val, 5, 4)
        grid.addWidget(m4_num, 5, 5)
        
        grid.addWidget(m5_lbl, 6, 1)
        grid.addWidget(m5_mag, 6, 2)
        grid.addWidget(m5_btn, 6, 3)
        grid.addWidget(m5_val, 6, 4)
        grid.addWidget(m5_num, 6, 5)
        
        grid.addWidget(m6_lbl, 7, 1)
        grid.addWidget(m6_mag, 7, 2)
        grid.addWidget(m6_btn, 7, 3)
        grid.addWidget(m6_val, 7, 4)
        grid.addWidget(m6_num, 7, 5)        
        
        self.setLayout(grid)    #Set the layout

        self.setGeometry(10, 100, 600, 300)
        self.setWindowTitle('Debug Motors')    
        self.show()

        self.fwd_left_thruster = m1_mag.value()
        self.fwd_right_thruster = m2_mag.value()
        self.bck_left_thruster = m3_mag.value()
        self.bck_right_thruster = m4_mag.value()
        self.front_thruster = m5_mag.value()
        self.back_thruster = m6_mag.value()        

    def flip(self):
        (self.fwd_left_thruster)
        #flip motor direction
        pass

    def stringedit(self):
        #display string format, change string format according to mx_num.value() 
        pass


    def stringcode():
        
        """
        Power: Overall scaling factor (0.4 = 40% of the full power)
        Fwd_factor: The power factor when moving forward/backward
        Side_factor: The power factor when turning around (yaw)

        The values for the four thrusters in the horizontal plane (fwd_left_thruster,
        fwd_right_thruster, bck_left_thruster and bck_right_thruster) is calculated by
        taking in the value of each of the joystic three main control axis (X, Y and Yaw)
        values and multplying each value by the appropriate scaling factor. These values
        are then added with respect to the relevant sign (+ve/-ve).

        This is a reasonable approximation; however, this calculation has a limited
        domain at which it is valid. Specfically, at each of the four joystick diagonal
        axis (i.e: when X AND Y are equal to 1 or -1) the resultant value goes beyond the
        boundaries (1100 and 1900). Therefore, a condition has been written to handle this
        problem by dividing the resultant value by 2 (e.g: 3800 becomes 1900). This is not
        a perfect scenario but it is acceptable for this application.
        """
        
        
        self.power = 0.4
        self.fwd_factor = 400 * self.power
        self.side_factor = 400 * self.power
        self.yaw_factor = 200

        # Account for double power in case of diagonals
        if ((self.X_Axis > 0.1 and self.Y_Axis < -0.1) or
            (self.X_Axis < -0.1 and self.Y_Axis > 0.1) or
                (self.X_Axis < -0.1 and self.Y_Axis < -0.1) or
                (self.X_Axis > 0.1 and self.Y_Axis > 0.1)):
            self.fwd_factor = 200 * self.power      # multiply by half of the power factor
            self.side_factor = 200 * self.power

        self.fwd_left_thruster = int(
            1500 - self.fwd_factor * self.Y_Axis - self.side_factor * self.X_Axis + self.yaw_factor * self.Yaw)
        self.fwd_right_thruster = int(
            1500 + self.fwd_factor * self.Y_Axis + self.side_factor * self.X_Axis + self.yaw_factor * self.Yaw)
        self.bck_left_thruster = int(
            1500 - self.fwd_factor * self.Y_Axis - self.side_factor * self.X_Axis + self.yaw_factor * self.Yaw)
        self.bck_right_thruster = int(
            1500 + self.fwd_factor * self.Y_Axis - self.side_factor * self.X_Axis + self.yaw_factor * self.Yaw)


        # To go up/down
        self.front_thruster = int(1500 + self.fwd_factor * self.Rudder)
        self.back_thruster = int(1500 + self.fwd_factor * self.Rudder)

        # ------Pitching code------
        """
        To pitch up/down the pilot needs to put the throttle in the +ve or -ve position. This overides
        the above 2 lines and moves the thrusters in oppsite directions in order to pitch as required.
        """
        if(self.Throttle>0.1 or self.Throttle<-0.1):
            self.front_thruster = int(1500 - self.fwd_factor * self.Throttle)
            self.back_thruster = int(1500 - self.fwd_factor * self.Throttle)        
        
        # Final string to be sent
        self.stringToSend = str([self.fwd_left_thruster, self.front_thruster, self.fwd_right_thruster,
                                 self.bck_right_thruster, self.back_thruster, self.bck_left_thruster,
                                 self.arm, self.funnel, self.BT_button1, LED1, LED2, PC, self.BT])
        #print(self.stringToSend) # Print final string    

def main():

    ex = Gui()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

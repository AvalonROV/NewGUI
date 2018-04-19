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
        fval_lbl = QLabel('Flip Value:'); fval_lbl.setStyleSheet(" font: bold; qproperty-alignment: AlignCenter")
        order_lbl = QLabel('Order in string'); order_lbl.setStyleSheet(" font: bold; qproperty-alignment: AlignCenter")
        
        m1_lbl = QLabel('Forward Left Motor')
        m2_lbl = QLabel('Forward Right Motor')
        m3_lbl = QLabel('Back Left Motor')
        m4_lbl = QLabel('Back Right Motor')
        m5_lbl = QLabel('Front Motor')
        m6_lbl = QLabel('Back Motor')

        self.m1_mag = QSpinBox(); self.m1_mag.setRange(-400, 400); self.m1_mag.setValue(0); self.m1_mag.valueChanged.connect(self.stringcode)
        self.m2_mag = QSpinBox(); self.m2_mag.setRange(-400, 400); self.m2_mag.setValue(0); self.m2_mag.valueChanged.connect(self.stringcode)
        self.m3_mag = QSpinBox(); self.m3_mag.setRange(-400, 400); self.m3_mag.setValue(0); self.m3_mag.valueChanged.connect(self.stringcode)
        self.m4_mag = QSpinBox(); self.m4_mag.setRange(-400, 400); self.m4_mag.setValue(0); self.m4_mag.valueChanged.connect(self.stringcode)
        self.m5_mag = QSpinBox(); self.m5_mag.setRange(-400, 400); self.m5_mag.setValue(0); self.m5_mag.valueChanged.connect(self.stringcode)
        self.m6_mag = QSpinBox(); self.m6_mag.setRange(-400, 400); self.m6_mag.setValue(0); self.m6_mag.valueChanged.connect(self.stringcode)

        m1_btn = QPushButton('Flip Direction'); m1_btn.clicked.connect(self.flipflt)
        m2_btn = QPushButton('Flip Direction'); m2_btn.clicked.connect(self.flipfrt)
        m3_btn = QPushButton('Flip Direction'); m3_btn.clicked.connect(self.flipblt)
        m4_btn = QPushButton('Flip Direction'); m4_btn.clicked.connect(self.flipbrt)
        m5_btn = QPushButton('Flip Direction'); m5_btn.clicked.connect(self.flipft)
        m6_btn = QPushButton('Flip Direction'); m6_btn.clicked.connect(self.flipbt)
        
        self.m1_val = QSpinBox(); self.m1_val.setValue(1); self.m1_val.setRange(-1, 1)
        self.m2_val = QSpinBox(); self.m2_val.setValue(1); self.m2_val.setRange(-1, 1)
        self.m3_val = QSpinBox(); self.m3_val.setValue(1); self.m3_val.setRange(-1, 1)
        self.m4_val = QSpinBox(); self.m4_val.setValue(1); self.m4_val.setRange(-1, 1)
        self.m5_val = QSpinBox(); self.m5_val.setValue(1); self.m5_val.setRange(-1, 1)
        self.m6_val = QSpinBox(); self.m6_val.setValue(1); self.m6_val.setRange(-1, 1)

        self.m1_num = QSpinBox(); self.m1_num.setRange(1, 6); self.m1_num.setValue(1)
        self.m2_num = QSpinBox(); self.m2_num.setRange(1, 6); self.m2_num.setValue(2)
        self.m3_num = QSpinBox(); self.m3_num.setRange(1, 6); self.m3_num.setValue(3)
        self.m4_num = QSpinBox(); self.m4_num.setRange(1, 6); self.m4_num.setValue(4)
        self.m5_num = QSpinBox(); self.m5_num.setRange(1, 6); self.m5_num.setValue(5)
        self.m6_num = QSpinBox(); self.m6_num.setRange(1, 6); self.m6_num.setValue(6)
        
        self.str_disp = QTextEdit('blank')
        str_disp_btn = QPushButton('Display String Order'); str_disp_btn.clicked.connect(self.stringcode)
        
        grid = QGridLayout()              #Create layout container
        
        grid.addWidget(name_lbl, 1, 1)
        grid.addWidget(val_lbl, 1, 2)
        grid.addWidget(btn_lbl, 1, 3)
        grid.addWidget(fval_lbl, 1, 4)
        grid.addWidget(order_lbl, 1, 5)
        
        grid.addWidget(m1_lbl, 2, 1)
        grid.addWidget(self.m1_mag, 2, 2)
        grid.addWidget(m1_btn, 2, 3)
        grid.addWidget(self.m1_val, 2, 4)
        grid.addWidget(self.m1_num, 2, 5)
        
        grid.addWidget(m2_lbl, 3, 1)
        grid.addWidget(self.m2_mag, 3, 2)
        grid.addWidget(m2_btn, 3, 3)
        grid.addWidget(self.m2_val, 3, 4)
        grid.addWidget(self.m2_num, 3, 5)
        
        grid.addWidget(m3_lbl, 4, 1)
        grid.addWidget(self.m3_mag, 4, 2)
        grid.addWidget(m3_btn, 4, 3)
        grid.addWidget(self.m3_val, 4, 4)
        grid.addWidget(self.m3_num, 4, 5)
        
        grid.addWidget(m4_lbl, 5, 1)
        grid.addWidget(self.m4_mag, 5, 2)
        grid.addWidget(m4_btn, 5, 3)
        grid.addWidget(self.m4_val, 5, 4)
        grid.addWidget(self.m4_num, 5, 5)
        
        grid.addWidget(m5_lbl, 6, 1)
        grid.addWidget(self.m5_mag, 6, 2)
        grid.addWidget(m5_btn, 6, 3)
        grid.addWidget(self.m5_val, 6, 4)
        grid.addWidget(self.m5_num, 6, 5)
        
        grid.addWidget(m6_lbl, 7, 1)
        grid.addWidget(self.m6_mag, 7, 2)
        grid.addWidget(m6_btn, 7, 3)
        grid.addWidget(self.m6_val, 7, 4)
        grid.addWidget(self.m6_num, 7, 5)       
        
        grid.addWidget(str_disp_btn, 9, 1)
        grid.addWidget(self.str_disp, 9, 2, 1, 4)
        
        self.setLayout(grid)    #Set the layout

        self.setGeometry(10, 100, 600, 300)
        self.setWindowTitle('Debug Motors')    
        self.show()    
        
    def flipflt(self):   #flip motor direction 
        if (self.m1_val.value() == 1):
            self.m1_val.setValue(-1)
        elif (self.m1_val.value() == -1):
            self.m1_val.setValue(1)
            
    def flipfrt(self):   #flip motor direction 
        if (self.m2_val.value() == 1):
            self.m2_val.setValue(-1)
        elif (self.m2_val.value() == -1):
            self.m2_val.setValue(1)

    def flipblt(self):   #flip motor direction 
        if (self.m3_val.value() == 1):
            self.m3_val.setValue(-1)
        elif (self.m3_val.value() == -1):
            self.m3_val.setValue(1)
        
    def flipbrt(self):   #flip motor direction 
        if (self.m4_val.value() == 1):
            self.m4_val.setValue(-1)
        elif (self.m4_val.value() == -1):
            self.m4_val.setValue(1)

    def flipft(self):    #flip motor direction 
        if (self.m5_val.value() == 1):
            self.m5_val.setValue(-1)
        elif (self.m5_val.value() == -1):
            self.m5_val.setValue(1)

    def flipbt(self):    #flip motor direction 
        if (self.m6_val.value() == 1):
            self.m6_val.setValue(-1)
        elif (self.m6_val.value() == -1):
            self.m6_val.setValue(1)   


    def stringcode(self):
        
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
        self.fltV= self.m1_val.value()
        self.frtV= self.m2_val.value()
        self.bltV= self.m3_val.value()
        self.brtV= self.m4_val.value()
        self.ftV= self.m5_val.value()
        self.btV= self.m6_val.value()
        
        self.flMag = self.m1_mag.value()
        self.frMag = self.m2_mag.value()
        self.blMag = self.m3_mag.value()
        self.brMag = self.m4_mag.value()
        self.fMag = self.m5_mag.value()
        self.bMag = self.m6_mag.value()            
        
        self.power = 0.4
        self.fwd_factor = 400 * self.power
        self.side_factor = 400 * self.power
        self.yaw_factor = 200
        
        
        self.fwd_left_thruster = int(
            1500 - (self.fltV)*(self.flMag))
        self.fwd_right_thruster = int(
            1500 + (self.frtV)*(self.frMag))
        self.bck_left_thruster = int(
            1500 - (self.bltV)*(self.blMag))
        self.bck_right_thruster = int(
            1500 + (self.brtV)*(self.brMag))


        # To go up/down
        self.front_thruster = int(1500 + (self.ftV)*self.fMag)
        self.back_thruster = int(1500 + (self.btV)*self.bMag)
        
        self.stringInitial = [self.fwd_left_thruster, self.fwd_right_thruster, self.bck_left_thruster,
                              self.bck_right_thruster, self.front_thruster, self.back_thruster]
        self.stringName = ['fwd_left_t', 'fwd_right_t', 'back_left_t', 'back_right_t', 'front_t', 'back_t']
        self.stringOrder = [self.m1_num.value()-1, self.m2_num.value()-1, self.m3_num.value()-1, 
                            self.m4_num.value()-1, self.m5_num.value()-1, self.m6_num.value()-1]
        
        self.stringThing = [self.stringInitial[i] for i in self.stringOrder]
        self.stringName = [self.stringName[i] for i in self.stringOrder]
        self.stringToSend = (str(self.stringThing) + '\n\n' + str(self.stringName))
        print(self.stringToSend)
        self.str_disp.setText(self.stringToSend)
        '''
        # Final string to be sent
        self.stringToSend = str([self.fwd_left_thruster, self.front_thruster, self.fwd_right_thruster,
                                 self.bck_right_thruster, self.back_thruster, self.bck_left_thruster])
        print(self.stringToSend) # Print final string    
        '''

def main():

    ex = Gui()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

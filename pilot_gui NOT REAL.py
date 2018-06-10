#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This code has been developed by Avalon ROV Team for participating in the MATE
ROV competition (https://www.marinetech.org/rov-competition-2/). This code is
a GUI used by the pilot in order to control the ROV and send/recieve important
information.
"""

#============== Imports ========================
import cv2
import sys
import numpy as np
from PyQt4.QtGui import*
from PyQt4.QtCore import *
from time import sleep


"""
PyGame is used to get and process data from the joystick.
"""


app = QApplication(sys.argv) # Creat a new QApplication object. This manages
                                # the GUI application's control flow and main
                                # settings.

# Global variables defining the ROV LEDs status
LB1 = 0
LB2 = 0
DPC = 0
DB1 = 0

class MGui(QWidget):
#base class of all user interface objects. 

    def __init__(self, parent=None):
        super(MGui, self).__init__()
        self.motorUI()         
        MGui.fltV = self.m1_val.value()
        MGui.frtV = self.m2_val.value()
        MGui.bltV = self.m3_val.value()
        MGui.brtV = self.m4_val.value()
        MGui.ftV = self.m5_val.value()
        MGui.btV = self.m6_val.value()

    def motorUI(self):
        
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

        self.setGeometry(10, 100, 900, 300)
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

        MGui.fltV = self.m1_val.value()
        MGui.frtV = self.m2_val.value()
        MGui.bltV = self.m3_val.value()
        MGui.brtV = self.m4_val.value()
        MGui.ftV = self.m5_val.value()
        MGui.btV = self.m6_val.value()
        
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
            1500 - (MGui.fltV)*(self.flMag))
        self.fwd_right_thruster = int(
            1500 + (MGui.frtV)*(self.frMag))
        self.bck_left_thruster = int(
            1500 - (MGui.bltV)*(self.blMag))
        self.bck_right_thruster = int(
            1500 + (MGui.brtV)*(self.brMag))


        # To go up/down
        self.front_thruster = int(1500 + (MGui.ftV)*self.fMag)
        self.back_thruster = int(1500 + (MGui.btV)*self.bMag)
        
        self.stringThrust = [self.fwd_left_thruster, self.fwd_right_thruster, self.bck_left_thruster,
                              self.bck_right_thruster, self.front_thruster, self.back_thruster]
        self.stringName = ['fwd_left_t', 'fwd_right_t', 'back_left_t', 'back_right_t', 'front_t', 'back_t']
        self.stringOrder = [self.m1_num.value()-1, self.m2_num.value()-1, self.m3_num.value()-1, 
                            self.m4_num.value()-1, self.m5_num.value()-1, self.m6_num.value()-1]
        self.stringFlip = [MGui.fltV, MGui.frtV, MGui.bltV, MGui.brtV, MGui.ftV, MGui.btV]
        self.stringThrust_s = [self.stringThrust[i] for i in self.stringOrder]
        self.stringName_s = [self.stringName[i] for i in self.stringOrder]
        self.stringFlip_s = [self.stringFlip[i] for i in self.stringOrder]
        self.stringToDisplay = (str(self.stringName_s)+ '\n' + str(self.stringThrust_s) + '\n' + str(self.stringFlip_s))
        print(self.stringThrust_s)
        self.str_disp.setText(self.stringToDisplay)
#---------------- beginning of main Gui class
class Gui(QWidget):
    """
    This class is the base class of all user interface objects. 
    """
    def __init__(self, parent=None):
        super(Gui, self).__init__()

        self.initUI()
        #self.motorWindow = MGui(self)
        
        self.string_formatter()
        # ------THREADING-----#
        """
        This is used to process the joystick data in the background
        """
        self.thread = Worker()  #Define a thread object
        self.connect(self.thread, SIGNAL('Hello'), self.information) # Connect the incoming signal from the
                                                                        # thread to the 'information' function
        self.thread.start() #Start the thread

        #video 
        self.video1 = Video(cv2.VideoCapture(0))        #an object of class Video(argument)
        self.video2 = Video(cv2.VideoCapture(0))        #edit integer to change feed source, 0 is webcam, 1 is videograbber
        self._timer = QTimer(self)
        self._timer.timeout.connect(self.play1)
        self._timer.timeout.connect(self.play2)
        self._timer.start(27)
        self.update()

    def play1(self):
        try:
            self.video1.captureNextFrame()
            self.video_frame1.setPixmap(
                self.video1.convertFrame())
            self.video_frame1.setScaledContents(True)
        except TypeError:
            print("No frame")

    def play2(self):
        try:
            self.video2.captureNextFrame()
            self.video_frame2.setPixmap(
                self.video2.convertFrame())
            self.video_frame2.setScaledContents(True)
        except TypeError:
            print("No frame")

    def initUI(self):

        #================ Definitions ========================
        self.video_frame1 = QLabel()
        self.video_frame2 = QLabel()
        self.video_frame1.setMaximumSize(8*90, 6*90)          #640, 480; 8:6
        self.video_frame2.setMaximumSize(8*90, 6*90)


        self.icon1 = colour_box("255, 0, 0")           #format is ("r, g, b")
        self.icon2 = colour_box("255, 0, 0")
        self.icon3 = colour_box("255, 0, 0")
        self.icon4 = colour_box("255, 0, 0")
        self.indicator1 = QLabel('Inflating lifting bag 1')
        self.indicator2 = QLabel('Inflating lifting bag 2')
        self.indicator3 = QLabel('Detatching lifting bag')
        self.indicator4 = QLabel('Dropping power circuit')
        
        self.depth_lbl = QLabel('Depth Reading:')
        self.IMUx_lbl = QLabel('IMU X Value')
        self.IMUy_lbl = QLabel('IMU Y Value')        
        self.depth_reading = QLineEdit()
        self.IMUx_reading = QLineEdit()
        self.IMUy_reading = QLineEdit()
        
        self.motor_debug_btn = QPushButton('MOTOR DEBUG')
        self.motor_debug_btn.clicked.connect(self.on_motor_btn_clicked)

        self.cam_slider1 = QSlider()
        self.cam_slider1.setRange(0, 5)
        self.cam_slider1.setTickPosition(3) #sets tick position to either side of the slider
        self.cam_slider2 = QSlider()
        self.cam_slider2.setRange(0, 5)
        self.cam_slider2.setTickPosition(3)
        
        self.recieved_string_label = QLabel()   #Create label for the text received from the ROV
        self.recieved_string_label.setText("String Recieved from ROV")  #Set Text
        self.recieved_string_txtbox = QTextEdit()   #Create a text box to store the data received from the ROV
        self.recieved_string_txtbox.setReadOnly(True)   #Set the text box to read only
        self.complete_recieved_string = ''

        self.user_input = QTextEdit()   #Create an empty text box for the pilot to write any notes


        #================ Layout ========================
        grid = QGridLayout()              #Create layout container
        grid.addWidget(self.video_frame1, 1, 1, 1, 2)
        grid.addWidget(self.video_frame2, 1, 4, 1, 2)

        grid.addWidget(self.cam_slider1, 1, 3, 1, 1)
        grid.addWidget(self.cam_slider2, 1, 6, 1, 1)

        grid.addWidget(self.indicator1, 6, 1, 1, 1)
        grid.addWidget(self.indicator2, 7, 1, 1, 1)
        grid.addWidget(self.indicator3, 8, 1, 1, 1)
        grid.addWidget(self.indicator4, 9, 1, 1, 1)
        grid.addWidget(self.icon1, 6, 2)
        grid.addWidget(self.icon2, 7, 2)
        grid.addWidget(self.icon3, 8, 2)
        grid.addWidget(self.icon4, 9, 2)
        grid.addWidget(self.depth_lbl, 11, 1)
        grid.addWidget(self.depth_reading, 11, 2)
        grid.addWidget(self.IMUx_lbl, 12, 1)
        grid.addWidget(self.IMUx_reading, 12, 2)
        grid.addWidget(self.IMUy_lbl, 13, 1)
        grid.addWidget(self.IMUy_reading, 13, 2)
        grid.addWidget(self.motor_debug_btn, 12, 4)
        self.setLayout(grid)    #Set the layout

        self.setGeometry(10, 200, 600, 300)
        self.setWindowTitle('Pilot GUI')    
        self.show()

    def on_motor_btn_clicked(self):
        self.motorWindow = MGui(self)
        
    #------------What is to follow should be moved into a seprate file----------------------------
    def string_formatter(self):
        # Initital values
        self.BT = 0
        self.funnel = 0
        self.arm = 0
        global LB1
        global LB2
        global DB1
        global DPC

        # ================================ Thrusters Power ================================
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
    
    def information(self):
        pass

#---------------- beginning of video class
class Video():
    def __init__(self,capture):
        self.capture = capture
        self.currentFrame=np.array([])

    def captureNextFrame(self):
        """                           
        capture frame and reverse RBG BGR and return opencv image                                      
        """
        ret, readFrame=self.capture.read()
        if(ret==True):
            self.currentFrame=cv2.cvtColor(readFrame,cv2.COLOR_BGR2RGB)

    def convertFrame(self):
        """     converts frame to format suitable for             """
        try:
            height,width=self.currentFrame.shape[:2]
            img=QImage(self.currentFrame,
                       width,
                       height,
                              QImage.Format_RGB888)
            img=QPixmap.fromImage(img)
            self.previousFrame = self.currentFrame
            return img
        except:
            return None
#---------------- end of video class

class colour_box(QLabel):
    #Constructor
    def __init__(self, box_colour):
        super(colour_box, self).__init__()
        self.setStyleSheet("background-color: rgb(" + box_colour + ")")

    def change_colour(self, box_colour):    #changes colour of QLabel to whatever colour is set using RGB format
        self.setStyleSheet("background-color: rgb(" + box_colour + ")")
#---------------- end of colour_box class for LED indicators


"""
This class is responsible for threading which means running two operations
simultaneously. It emits a signal to define when the above program should be
updated
"""

class Worker(QThread):

    def __init__(self):
        QThread.__init__(self, parent=app)


def main():

    ex = Gui()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

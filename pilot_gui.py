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
import pygame
from time import sleep
from avalon_frontend import ROV
import converttobinary
import UndistortAND_Distance_Detection


"""
PyGame is used to get and process data from the joystick.
"""

pygame.init()   # Initialise PyGame
my_joystick = pygame.joystick.Joystick(0)   # Create a joystick object
my_joystick.init()  # Initialise the Joystick
clock = pygame.time.Clock() # Create a clock object to track time

app = QApplication(sys.argv) # Creat a new QApplication object. This manages
                                # the GUI application's control flow and main
                                # settings.
LB1 = 0
DB1 = 0
DB2 = 0
GRAB = 0
EM1 = 0
EM2 = 0
LEVELM = 0

class MGui(QWidget):
#base class of all user interface objects. 

    def __init__(self, parent=None):
        super(MGui, self).__init__()
        self.motorUI()         
        #MGui.fltV = self.m1_val.value()
        #MGui.frtV = self.m2_val.value()
        #MGui.bltV = self.m3_val.value()
        #MGui.brtV = self.m4_val.value()
        #MGui.ftV = self.m5_val.value()
        #MGui.btV = self.m6_val.value()

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
        
        self.m1_val = QSpinBox(); self.m1_val.setValue(Gui.fltV); self.m1_val.setRange(-1, 1)
        self.m2_val = QSpinBox(); self.m2_val.setValue(Gui.frtV); self.m2_val.setRange(-1, 1)
        self.m3_val = QSpinBox(); self.m3_val.setValue(Gui.bltV); self.m3_val.setRange(-1, 1)
        self.m4_val = QSpinBox(); self.m4_val.setValue(Gui.brtV); self.m4_val.setRange(-1, 1)
        self.m5_val = QSpinBox(); self.m5_val.setValue(Gui.ftV); self.m5_val.setRange(-1, 1)
        self.m6_val = QSpinBox(); self.m6_val.setValue(Gui.btV); self.m6_val.setRange(-1, 1)

        self.m1_num = QSpinBox(); self.m1_num.setRange(1, 6); self.m1_num.setValue(Gui.fltO)
        self.m2_num = QSpinBox(); self.m2_num.setRange(1, 6); self.m2_num.setValue(Gui.frtO)
        self.m3_num = QSpinBox(); self.m3_num.setRange(1, 6); self.m3_num.setValue(Gui.bltO)
        self.m4_num = QSpinBox(); self.m4_num.setRange(1, 6); self.m4_num.setValue(Gui.brtO)
        self.m5_num = QSpinBox(); self.m5_num.setRange(1, 6); self.m5_num.setValue(Gui.ftO)
        self.m6_num = QSpinBox(); self.m6_num.setRange(1, 6); self.m6_num.setValue(Gui.btO)
        
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
        self.stringOrderNumbers = [self.m1_num.value(), self.m2_num.value(), self.m3_num.value(), 
                            self.m4_num.value(), self.m5_num.value(), self.m6_num.value()]
        self.stringFlip = [MGui.fltV, MGui.frtV, MGui.bltV, MGui.brtV, MGui.ftV, MGui.btV]
        self.stringThrust_s = [self.stringThrust[i] for i in self.stringOrder]
        self.stringName_s = [self.stringName[i] for i in self.stringOrder]
        self.stringFlip_s = [self.stringFlip[i] for i in self.stringOrder]
        self.stringToDisplay = (str(self.stringName_s)+ '\n' + str(self.stringThrust_s) + '\n' + str(self.stringFlip_s))
        print(self.stringThrust_s)
        self.str_disp.setText(self.stringToDisplay)
        
        
        with open("order.txt", "w") as ofile:
            ofile.write(str(self.stringOrderNumbers))
        with open("flip.txt", "w") as ffile:
            ffile.write(str(self.stringFlip))


#---------------- beginning of main Gui class
class Gui(QWidget):
    """
    This class is the base class of all user interface objects. 
    """
    def __init__(self, parent=None):
        super(Gui, self).__init__()

        self.initUI()
        with open("order.txt", "r") as ofile:
            odata = eval(ofile.readline())

        Gui.fltO = odata[0]
        Gui.frtO = odata[1]
        Gui.bltO = odata[2]
        Gui.brtO = odata[3]
        Gui.ftO = odata[4]
        Gui.btO = odata[5]

        with open("flip.txt", "r") as ffile:
            fdata = eval(ffile.readline())
            
        Gui.fltV = fdata[0]
        Gui.frtV = fdata[1]
        Gui.bltV = fdata[2]
        Gui.brtV = fdata[3]
        Gui.ftV = fdata[4]
        Gui.btV = fdata[5]


        #self.motorWindow = MGui(self)
        
        self.frontend = ROV("127.0.0.1", 8000)

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
        self.video1 = Video(cv2.VideoCapture("http://192.168.1.5:8081"))        #an object of class Video(argument)
        self.video2 = Video(cv2.VideoCapture("http://192.168.1.5:8082"))
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
        self.icon5 = colour_box("255, 0, 0")
        self.indicator1 = QLabel('Inflating lifting bag')
        self.indicator2 = QLabel('Detaching lifting bag 1 Magnet')
        self.indicator3 = QLabel('Detaching lifting bag 2 Magnet')
        self.indicator4 = QLabel('Grabber enabled?')
        self.indicator5 = QLabel('Levelling motor')
        
        self.depth_lbl = QLabel('Depth Reading:')
        self.IMUx_lbl = QLabel('IMU X Value')
        self.IMUy_lbl = QLabel('IMU Y Value')        
        self.depth_reading = QLineEdit()
        self.IMUx_reading = QLineEdit()
        self.IMUy_reading = QLineEdit()
        self.IMU_txt = QTextEdit()
        
        self.motor_debug_btn = QPushButton('MOTOR DEBUG')
        self.motor_debug_btn.clicked.connect(self.on_motor_btn_clicked)

        self.length_det_btn = QPushButton('Length Detection Enable')
        self.length_det_btn.clicked.connect(self.screenshot_and_length)        

        self.cam_slider1 = QSlider()
        self.cam_slider1.setRange(0, 4)
        self.cam_slider1.setTickPosition(0) #sets tick position to either side of the slider
        self.cam_slider1.valueChanged.connect(self.on_slider1_changed)
        self.cam_slider2 = QSlider()
        self.cam_slider2.setRange(0, 4)
        self.cam_slider2.setTickPosition(0)
        self.cam_slider2.setSliderPosition(1)
        self.cam_slider2.valueChanged.connect(self.on_slider2_changed)
        
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
        grid.addWidget(self.indicator5, 10, 1, 1, 1)
        grid.addWidget(self.icon1, 6, 2)
        grid.addWidget(self.icon2, 7, 2)
        grid.addWidget(self.icon3, 8, 2)
        grid.addWidget(self.icon4, 9, 2)
        grid.addWidget(self.icon5, 10, 2)
        grid.addWidget(self.depth_lbl, 11, 1)
        grid.addWidget(self.depth_reading, 11, 2)
        grid.addWidget(self.IMUx_lbl, 12, 1)
        grid.addWidget(self.IMUx_reading, 12, 2)
        grid.addWidget(self.IMUy_lbl, 13, 1)
        grid.addWidget(self.IMUy_reading, 13, 2)
        grid.addWidget(self.IMU_txt, 9, 4, 2, 2)

        grid.addWidget(self.motor_debug_btn, 12, 4)
        grid.addWidget(self.length_det_btn, 13, 5)
        self.setLayout(grid)    #Set the layout

        self.setGeometry(10, 200, 600, 300)
        self.setWindowTitle('Pilot GUI')    
        self.show()

    def on_motor_btn_clicked(self):
        self.motorWindow = MGui(self)

    def screenshot_and_length(self):
        cv2.imwrite("test1.png", self.video1.currentFrame)
        self.detect_length = UndistortAND_Distance_Detection.Example()

    def on_slider1_changed(self):
        if (self.cam_slider1.value() ==0):
            self.video1 = Video(cv2.VideoCapture("http://192.168.1.5:8081"))
        if (self.cam_slider1.value() ==1):
            self.video1 = Video(cv2.VideoCapture("http://192.168.1.5:8082"))
        if (self.cam_slider1.value() ==2):
            self.video1 = Video(cv2.VideoCapture("http://192.168.1.5:8083"))
        if (self.cam_slider1.value() ==3):
            self.video1 = Video(cv2.VideoCapture("http://192.168.1.5:8084"))
        if (self.cam_slider1.value() ==4):
            self.video1 = Video(cv2.VideoCapture("http://192.168.1.5:8085"))
        else:
            pass
        #self._timer = QTimer(self)
        self._timer.timeout.connect(self.play1)
        #self._timer.start(27)
    
    def on_slider2_changed(self):
        if (self.cam_slider2.value() ==0):
            self.video2 = Video(cv2.VideoCapture("http://192.168.1.5:8081"))
        if (self.cam_slider2.value() ==1):
            self.video2 = Video(cv2.VideoCapture("http://192.168.1.5:8082"))
        if (self.cam_slider2.value() ==2):
            self.video2 = Video(cv2.VideoCapture("http://192.168.1.5:8083"))
        if (self.cam_slider2.value() ==3):
            self.video2 = Video(cv2.VideoCapture("http://192.168.1.5:8084"))
        if (self.cam_slider2.value() ==4):
            self.video2 = Video(cv2.VideoCapture("http://192.168.1.5:8085"))
        else:
            pass
        #self._timer = QTimer(self)
        self._timer.timeout.connect(self.play2)
        self._timer.start(27)
        
    #------------What is to follow should be moved into a seprate file----------------------------
    def string_formatter(self):
        """
        This function formats the string that will be sent to the ROV containg the
        commands.

        The format of the string is: [FL, FU, FR, BR, BU, BL, ARM, FUN, LB1, DB1, DPC, BT]
DB
        FL: Forward Left Thruster 
        FU: Forward Up Thruster
        FR: Forward Right Thruster
        BR: Backward Right Thruster
        BU: Backward Up Thruster
        BL: Backward Left Thruster
        Thrusters values are between 1100 and 1900, with 1500 being nominal (at rest).

        0 -> not moving
        1 -> clockwise/opening
        2 -> anti-clockwise/closing

        DPC: power circuit dropped indicator
        LB1: lifting bag 1
        DB1: drop bag 1
        
        0 -> OFF
        1 -> ON


        BT: Bluetooth
        """
        # ------ Storing the values from the different axis on joystick------#
        self.X_Axis = my_joystick.get_axis(0)  # X_Axis- Axis 0
        self.Y_Axis = my_joystick.get_axis(1)  # Y_Axis - Axis 1
        self.Throttle = my_joystick.get_axis(2)
        self.Yaw = my_joystick.get_axis(3)
        self.Rudder = my_joystick.get_axis(4)
        self.one_button = my_joystick.get_button(0)  # Button 1
        self.GRAB_button = my_joystick.get_button(1)  # Button 2
        self.three_button = my_joystick.get_button(2)  # Button 3
        self.EM1_button = my_joystick.get_button(4)  # Button 5
        self.EM2_button = my_joystick.get_button(5)  # Button 6
        self.LB1_button = my_joystick.get_button(6)  # Button 7
        self.SE_button = my_joystick.get_button(10)  # Button SE
        self.ST_button = my_joystick.get_button(11)  # Button ST
        self.LEVELM_button = my_joystick.get_button(7)  # Button 8
        self.four_button = my_joystick.get_button(3)  # Button 4, L3


        # Initital values
        # blah like self.funnel = 0 or global LB1
        # self.LB1 = 0
        # self.DB1 = 0
        # self.GRAB = 0
        # self.EM1 = 0
        # self.EM2 = 0
        global LB1
        global DB1
        global DB2
        global GRAB
        global EM1
        global EM2
        global LEVELM

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
        if ((self.X_Axis > 0.1 and self.Y_Axis < -0.1) or
            (self.X_Axis < -0.1 and self.Y_Axis > 0.1) or
                (self.X_Axis < -0.1 and self.Y_Axis < -0.1) or
                (self.X_Axis > 0.1 and self.Y_Axis > 0.1)):
            self.fwd_factor = 200 * self.power      # multiply by half of the power factor
            self.side_factor = 200 * self.power
            
        self.fwd_left_thruster = int(
            1500 - (self.fltV)*(self.fwd_factor * self.Y_Axis - self.side_factor * self.X_Axis + self.yaw_factor * self.Yaw))
        self.fwd_right_thruster = int(
            1500 + (self.frtV)*(self.fwd_factor * self.Y_Axis + self.side_factor * self.X_Axis + self.yaw_factor * self.Yaw))
        self.bck_left_thruster = int(
            1500 - (self.bltV)*(self.fwd_factor * self.Y_Axis - self.side_factor * self.X_Axis + self.yaw_factor * self.Yaw))
        self.bck_right_thruster = int(
            1500 + (self.brtV)*(self.fwd_factor * self.Y_Axis - self.side_factor * self.X_Axis + self.yaw_factor * self.Yaw))


        # To go up/down
        self.front_thruster = int(1500 + (self.ftV)*(self.fwd_factor * self.Rudder))
        self.back_thruster = int(1500 + (self.btV)*(self.fwd_factor * self.Rudder))

        # ------Pitching code------
        """
        To pitch up/down the pilot needs to put the throttle in the +ve or -ve position. This overides
        the above 2 lines and moves the thrusters in oppsite directions in order to pitch as required.
        """
        if(self.Throttle>0.1 or self.Throttle<-0.1):
            self.front_thruster = int(1500 - (self.ftV)*(self.fwd_factor * self.Throttle))
            self.back_thruster = int(1500 - (self.btV)*(self.fwd_factor * self.Throttle))


        # ================================ Manipulators ================================

        # LB1
        if (self.LB1_button == 1):
            self.frontend.set_lift_bag_inflate(1)
            self.icon1.change_colour("255, 0, 0")
        else:
            LB1 = 0
            self.frontend.set_lift_bag_inflate(0)
            self.icon1.change_colour("0, 255, 0")


        # EM1
        if (self.EM1_button == 1):
            EM1 = 1
            self.frontend.set_lift_bag_EM_release(EM1, 0)
            self.icon2.change_colour("255, 0, 0")
        else:
            EM1 = 0
            self.frontend.set_lift_bag_EM_release(EM1, 0)
            self.icon2.change_colour("0, 255, 0")


        # EM2
        if (self.EM2_button == 1):
            EM2 = 1
            self.frontend.set_lift_bag_EM_release(EM2, 1)
            self.icon3.change_colour("255, 0, 0")
        else:
            EM2 = 0
            self.frontend.set_lift_bag_EM_release(EM2, 1)
            self.icon3.change_colour("0, 255, 0")


        # # DB1
        # if (self.DB1_button == 1):
        #     DB1 = 0
        #     self.frontend.set_lift_bag_release(DB1, 0)
        #     self.icon4.change_colour("255, 0, 0")
        # else:
        #     DB1 = 1
        #     self.frontend.set_lift_bag_release(DB1, 0)
        #     self.icon4.change_colour("0, 255, 0")
        #
        # # DB2
        # if (self.DB2_button == 1):
        #     DB2 = 0
        #     self.frontend.set_lift_bag_release(DB2, 1)
        #     self.icon5.change_colour("255, 0, 0")
        # else:
        #     DB2 = 1
        #     self.frontend.set_lift_bag_release(DB2, 1)
        #     self.icon5.change_colour("0, 255, 0")

        # GRAB
        if (self.GRAB_button == 1):
            GRAB = 1
            self.frontend.set_grabber_position(1)
            self.icon4.change_colour("255, 0, 0")
        else:
            GRAB = 0
            self.frontend.set_grabber_position(0)
            self.icon4.change_colour("0, 255, 0")


        # LEVELM
        if (self.LEVELM_button == 1):
            LEVELM = 1
            self.frontend.set_levelling_motor_rotation(1)
            self.icon5.change_colour("255, 0, 0")
        else:
            LEVELM = 0
            self.frontend.set_levelling_motor_rotation(0)
            self.icon5.change_colour("0, 255, 0")


        with open("order.txt", "r") as ofile:
            order_data = eval(ofile.readline())
            
        thruster_string = [self.fwd_left_thruster, self.front_thruster, self.fwd_right_thruster,
                           self.bck_right_thruster, self.back_thruster, self.bck_left_thruster]
        self.thruster_string_ordered = [thruster_string[i-1] for i in order_data]
        self.frontend.set_thrusts(self.thruster_string_ordered)
        #print(thruster_string)


    def information(self):
        """
        This function reads parameters from the joystick and sends the formatted string to the ROV.
        """
        name_joystick = my_joystick.get_name()  # Collects the pre-defined name of joystick
        number_axes = my_joystick.get_numaxes()  # Collects the pre-defined number of axis
        number_buttons = my_joystick.get_numbuttons()  # Collects the pre-defined number of buttons


        try:    # Read data from the ROV
            var = self.frontend.recieve_message().decode()
            if (var[0] == 'w'):
                self.IMU_txt.setText(var[1:])
            if (var[0] == 'd'):
                self.depth_reading.setText(str(var[1:]))
            else:
                print(var)
        except:
            print("pass")
            pass

        self.string_formatter()  # Calling the thruster value
        self.frontend.send_settings()   # send settings including parameters
        self.set_values()
        
    def set_values(self):
        self.depth_reading.setText(str(self.frontend.get_depth()))
        x_value = self.frontend.get_imu()[0]
        y_value = self.frontend.get_imu()[1]
        self.IMUx_reading.setText(str(x_value))
        self.IMUy_reading.setText(str(y_value))
        

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

    def run(self):
        EXIT = False
        while not EXIT:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    EXIT = True
            self.emit(SIGNAL('Hello'))
            clock.tick(30) #This determines how fast the frames change per second
        pygame.quit() # This is used to quit pygame and use any internal program within the python
        quit()

def main():
    
    ex = Gui()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

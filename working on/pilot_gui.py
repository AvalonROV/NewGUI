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


"""
PyGame is used to get and proces data from the joystick.
"""

pygame.init()   # Initialise PyGame
my_joystick = pygame.joystick.Joystick(0)   # Create a joystick object
my_joystick.init()  # Initialise the Joystick
clock = pygame.time.Clock() # Create a clock object to track time

app = QApplication(sys.argv) # Creat a new QApplication object. This manages
                                # the GUI application's control flow and main
                                # settings.

# Global variables defining the ROV LEDs status
LB1 = 0
LB2 = 0
DPC = 0
DB1 = 0


class Gui(QWidget):
    """
    This class is the base class of all user interface objects. 
    """
    def __init__(self):
        super(Gui, self).__init__()

        self.initUI()
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
        title1_font = QFont("Arial", 16, QFont.Bold)    #Define title1 font

        # Title
        application_title = QLabel()                        #Create label for the window title
        application_title.setText("ROV Control Interface")  #Set Text
        application_title.setFont(title1_font)              #Set font
        application_title.setAlignment(Qt.AlignCenter)      #Set Allignment

        self.video_frame1 = QLabel()
        self.video_frame2 = QLabel()
        self.video_frame1.setMaximumSize(8*70, 6*70)          #640, 480; 8:6
        self.video_frame2.setMaximumSize(8*70, 6*70)


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
        self.setLayout(grid)    #Set the layout

        self.setGeometry(10, 100, 600, 300)
        self.setWindowTitle('Pilot GUI')    
        self.show()

    #------------What is to follow should be moved into a seprate file----------------------------
    def string_formatter(self):
        """
        This function formats the string that will be sent to the ROV containg the
        commands.

        The format of the string is: [FL, FU, FR, BR, BU, BL, ARM, FUN, LB1, LB2,DB1, DPC, BT]
DB
        FL: Forward Left Thruster 
        FU: Forward Up Thruster
        FR: Forward Right Thruster
        BR: Backward Right Thruster
        BU: Backward Up Thruster
        BL: Backward Left Thruster
        Thrusters values are between 1100 and 1900, with 1500 being nominal (at rest).

        ARM: Manipulator Arm
        FUN: Funnel
        0 -> not moving
        1 -> clockwise/opening
        2 -> anti-clockwise/closing

        DPC: power circuit dropped indicator
        LB1: lifting bag 1
        LB2: lifting bag 2
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
        self.LB1_button = my_joystick.get_button(4)  # Button 5
        self.LB2_button = my_joystick.get_button(5)  # Button 6
        self.DB1_button = my_joystick.get_button(6)  # Button 7
        self.buttonSE = my_joystick.get_button(10)  # Button SE
        self.buttonST = my_joystick.get_button(11)  # Button ST
        self.DPC_button = my_joystick.get_button(7)  # Button 8
        self.button4 = my_joystick.get_button(3)  # Button 4, L3


        # Bluetooth controls
        self.BT_button1 = my_joystick.get_button(0)
        self.BT_button2 = my_joystick.get_button(1)

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


        # ================================ Manipulators ================================

        # LB1
        if (self.LB1_button == 1):
            sleep(0.2)
            if (LB1 == 1):
                LB1 = 0
                self.icon1.change_colour("0, 255, 0")
            else:
                LB1 = 1
                self.icon1.change_colour("0, 255, 0")


        # LB2
        if (self.LB2_button == 1):
            sleep(0.2)
            if (LB2 == 1):
                LB2 = 0
                self.icon2.change_colour("0, 255, 0")
            else:
                LB2 = 1
                self.icon2.change_colour("0, 255, 0")

                
        # DB1
        if (self.DB1_button == 1):
            sleep(0.2)
            if (DB1 == 1):
                DB1 = 0
                self.icon3.change_colour("255, 0, 0")
            else:
                DB1 = 1
                self.icon3.change_colour("0, 255, 0")


        # DPC
        if (self.DPC_button == 1):
            sleep(0.2)
            if (DPC == 1):
                DPC = 0
                self.icon4.change_colour("255, 0, 0")
            else:
                DPC = 1
                self.icon4.change_colour("0, 255, 0")



        # Bluetooth
        if(self.BT_button1 == 1):
            self.BT = 1
        elif(self.BT_button2 == 1):
            self.BT = 2

        # Final string to be sent
        self.stringToSend = str([self.fwd_left_thruster, self.front_thruster, self.fwd_right_thruster,
                                 self.bck_right_thruster, self.back_thruster, self.bck_left_thruster,
                                 self.arm, self.funnel, self.BT_button1, LB1, LB2,DB1, DPC, self.BT])
        #print(self.stringToSend) # Print final string

    def information(self):
        """
        This function reads parameters from the joystick and sends the formatted string to the ROV.
        """
        name_joystick = my_joystick.get_name()  # Collects the pre-defined name of joystick
        number_axes = my_joystick.get_numaxes()  # Collects the pre-defined number of axis
        number_buttons = my_joystick.get_numbuttons()  # Collects the pre-defined number of buttons

        try:    # Read data from the ROV
            recieved_string = recieve_socket.recv(1024).decode()
            self.complete_recieved_string += recieved_string + '\n'
            self.recieved_string_txtbox.setText(self.complete_recieved_string)
        except:
            pass

        self.string_formatter()  # Calling the thruster value



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
#---------------- end of colour_box classes for LED indicators


"""
This class is responsible for threading which means runnin two operations
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

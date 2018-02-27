import sys
from PyQt4.QtGui import*
from PyQt4.QtCore import *
import pygame

#pygame.init()   
#my_joystick = pygame.joystick.Joystick(0)  
#my_joystick.init() 
#Initialising pygame, creating, and initialising joystick

app = QApplication(sys.argv)

class Window(QWidget):
    
    def __init__(self):
        super(Window, self).__init__()
        self.initUI()           #all the different methods that need to be initialised

    def initUI(self):
        # Title
        title1_font = QFont("Arial", 16, QFont.Bold)    #Define title1 font
        application_title = QLabel()                        #Create label for the window title
        application_title.setText("ROV Control Interface")  #Set Text
        application_title.setFont(title1_font)              #Set font
        application_title.setAlignment(Qt.AlignCenter)      #Set Allignment        
        
        #Define all widgets etc.
        self.LEDs_label = QLabel("Indicators")
        self.led1_label = QLabel('inflate')
        self.led2_label = QLabel('detatch')
        self.led1_indicator = QLabel() 	#one for each indicator needed
        self.led2_indicator = QLabel()
        self.redcircle_indicator = QPixmap("red.png")
        self.greencircle_indicator = QPixmap("green.png")
        self.led1_indicator.setPixmap(self.redcircle_indicator)
        self.led2_indicator.setPixmap(self.redcircle_indicator) #initialise both as red

        vbox = QVBoxLayout()
        vbox.addWidget(application_title)
        vbox.addWidget(self.LEDs_label)
        
        LEDs_hbox = QHBoxLayout()           #Create layout container
        LEDs_hbox.addWidget(self.led1_label)#Populate the container
        LEDs_hbox.addWidget(self.led1_indicator)
        LEDs_hbox.addWidget(self.led2_label)
        LEDs_hbox.addWidget(self.led2_indicator)
    
        vbox.addLayout(LEDs_hbox)
        
        recieved_string_box = QHBoxLayout() #Create layout container
        vbox.addLayout(recieved_string_box)
    
        self.setLayout(vbox)    #Set the layout
    
        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle('Buttons')    
        self.show()
        
        
def main():
          
    ex = Window()
    sys.exit(app.exec_())
        
        
if __name__ == '__main__':
    main()

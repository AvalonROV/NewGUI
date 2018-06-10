# -*- coding: utf-8 -*-
"""
This is the code for the Avalon ROV Project Frontend. This software performs communications with the ROV
using a UDP Ethernet configuration. The Frontend makes it easier for the main UI to communicate with the
ROV by providing a layer of abstraction between the two main system sections.

AUTHOR: Sam Maxwell
DATE RELEASED: PLEASE FILL ON RELEASE
VERSION: PLEASE FILL ON RELEASE
"""
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
#MODULES
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
import socket    #UDP Communication Module
import converttobinary as ctb    #Module that handles conversion of Python Values to Binary

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
#DEFINITIONS
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------


#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
#CLASSES
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
#The class that performs the main control functions with the ROV
class ROV():
    """
    A class used to facilitate communications with the Avalon ROV. UDP Communication is used via an Ethernet Interface to
    communiacte with the ROV. Standard ROV Parameters:
    
    ROV IP Address: 192.168.1.5
    ROV Port: 8000
    
    """
    #Communication Definitions
    com_buff_size = 1024                                #The size of the buffer used to recieve message from the ROV
    
    #Thruster Parameters
    thrust_vals = [0, 0, 0, 0, 0, 0]                    #A List containing the raw values for each thruster
    
    #IMU Parameters
    imu_vals = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]           #A List containing the values from the IMU
    
    #Movement Parameters
    depth_current = 0.0                                 #A Value containing the ROVs current depth
    axis_stabilisation_flags = [0, 0, 0, 0, 0]          #A List containing the flags to enable/disable stabilisation on each axis
    
    #Lifting Bag Parameters
    release_mechanism_states = [0, 0]                   #A List containing the flags to open/close individual release mechanisms
    inflate_mechanism_state = [0]                       #A Value that indicates whether the inflation system is enabled/disabled
    EM_release_mechanism_states = [0, 0]                   #A List containing the flags to open/close EM release mechanisms

    #Grabber Parameters
    grabber_val = [0]                                     #A Value that contains the percentage the grabber is open
    
    #Platform Levelling Parameters
    platform_imu_vals = [0.0, 0.0]                      #A List containg the values from the seismometer platform IMU
    levelling_motor_flag = [0]                            #A Value that contains the direction of rotation of the leveling motor
    
    #Camera Parameters
    camera_one_index = [0]                                #A Value that contains the index of the camera to be shown on feed 1
    camera_two_index = [0]                                #A Value that contains the index of the camera to be shown on feed 2
    
    #Emergency Stop Values
    emergency_thrust_flag = [0]                           #A Value that indicates whether the emergency thruster stop is enabled/disabled
    
    #MAIN COMMUNICATION METHODS
    #Constructor, initialises communication with the ROV
    def __init__(self, rov_ip, rov_port):
        """
        PURPOSE: Initialises UDP Communication with the ROV.
        INPUTS: rov_ip = A string containing the ROV's IP Address
                rov_port = An integer containing the ROV's UDP Port
        OUTPUTS: NONE
        """
        #Informing User of selected IP Address and Port
        print ("Target IP Address: " + rov_ip)
        print ("Target Port: " + str(rov_port))
        
        #Connecting to the ROV
        self.rov_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  #Specifies Internet and UDP Communication to the Socket Class
        #self.rov_socket.bind((rov_ip, rov_port))
        
        #Performing a test communication with the ROV
        
        #Saving the ROV's IP Address and Port
        self.ip_address = rov_ip
        self.port = rov_port
    
    #Method used to send a message via UDP to the ROV
    def send_message(self, message):
        """
        PURPOSE: Send a single message to the ROV via the UDP Communication Socket
        INPUTS: message = A string that contains the message to be sent to the ROV
        OUTPUTS: NONE
        """
        #print(message)
        self.rov_socket.sendto(message, (self.ip_address, self.port))
    
    #Method used to recieve a message via UDP from the ROV
    def recieve_message(self):
        """
        PURPOSE: Recieve a message from the ROV
        INPUTS: NONE
        OUTPUTS: The message sent by the ROV as a string
        """
        message = self.rov_socket.recv(self.com_buff_size)
        return message
    
    #Method used to perform the Send communication cycle with the ROV
    def send_settings(self):
        """
        PURPOSE: Performs the ROV Send Communication Cycle
        INPUTS: NONE
        OUTPUTS: Outputs 1 if the Send Cycle completes successfully, Outputs 0 if the Send Cycle fails
        """

        message_list = []

        message_string = ""

        message_list = (message_list+ self.thrust_vals + self.axis_stabilisation_flags + self.release_mechanism_states
                        + self.inflate_mechanism_state + self.grabber_val + self.levelling_motor_flag
                        + self.camera_one_index + self.camera_two_index)

        '''
        #Encoding and Appending Thruster Values to message string
        message_string += str(self.thrust_vals)
        
        #Encoding and Appending the Stabilisation Flags to the message string
        message_string += str(self.axis_stabilisation_flags)
        
        #Encoding and Appending the Release Mechanism Flags to the message string
        message_string += str(self.release_mechanism_states)
        
        #Encoding and Appending the Inflation Mechanism State to the message string
        message_string += str(self.inflate_mechanism_state)
        
        #Encoding and Appending the Grabber Position to the message string
        message_string += str(self.grabber_val)
        
        #Encoding and Appending the Levelling Motor Flag to the message string
        message_string += str(self.levelling_motor_flag)
        
        #Encoding and Appending the Camera Index Values to the message string
        message_string += str(self.camera_one_index) + str(self.camera_two_index)
        '''
        print(message_list)
        message_string = str(message_list)
        #Sending the Message to the ROV
        self.send_message(message_string.encode())        
        #print(message_string)
        
    #Method used to perform the Recieve communication cycle with the ROV
    def recieve_parameters(self):
        """
        PURPOSE: Performs the ROV Recieve Communication Cycle
        INPUTS: NONE
        OUTPUTS: Outputs 1 if the Recieve Cycle completes successfully, Outputs 0 if the Recieve Cycle fails
        """
        #Recieving the latest data from the ROV
        message_string = self.recieve_message()
        
        #Decoding the IMU Values from the Message String
        self.decode_imu_vals(message_string[0:48])
    
    #Method used to perform the full communication cycle with the ROV
    def communicate(self):
        """
        PURPOSE: Performs full ROV Communication Cycle, including Send and Recieve
        INPUTS: NONE
        OUTPUTS: Outputs 1 if the communication cycle was successful, Outputs 0 if the communication cycle failed        
        """
        print ("Performing ROV Communication Cycle")
    
    #ENCODING METHODS
    #Method used to encode a thruster value for transmission to the ROV
    def encode_thrust_val(self, thruster_val_index):
        """
        PURPOSE: Encodes a single ROV Thrust value into a C Binary Value
        INPUTS: thruster_val_index = The index of the thruster value that needs to be encoded
        OUTPUTS: encoded_val = The encoded thruster value as a C Short represented as a Python String
        """
        #Getting the current thrust value for the given thruster
        thruster_val = self.thrust_vals[thruster_val_index]
        
        #Encoding the thruster value
        encoded_val = ctb.short_pack(thruster_val)
        return encoded_val
    
    #Method used to encode all thruster values and return as a list
    def encode_all_thrusts(self):
        """
        PURPOSE: Encodes all ROV Thrust values into a single message string
        INPUTS: NONE
        OUTPUTS: encoded_thrust_vals = The Thruster values encoded as C Shorts represented by a Python String
        """
        encoded_thrust_vals = ""
        
        for thruster_index in range(0, len(self.thrust_vals)):
            #Encoding the current thrust value
            print(self.encode_thrust_val(thruster_index))
            encoded_thrust_vals += self.encode_thrust_val(thruster_index).decode()

        return encoded_thrust_vals
    
    #Method used to encode axis stabilisation flags into an individual Byte
    def encode_stabilisation_flags(self):
        """
        PURPOSE: Encodes the axis stabilisation flags into a single C Character Byte represented as a Python String
        INPUTS: NONE
        OUTPUTS: encoded_byte = The stabilisation flags encoded as a single Byte represented as a Python String
        """
        encoded_byte = 0
        num_flags = len(self.axis_stabilisation_flags) - 1
        
        #Converting the flags list into an Integer containing the Flags in the Same Order [0, 1, 1] ==> 011
        for index, stabilisation_flag in enumerate(self.axis_stabilisation_flags):
            index = num_flags - index
            encoded_byte |= (stabilisation_flag << index)
        
        #Packing the Python Integer into a C Char
        encoded_byte = ctb.char_pack(encoded_byte)
        return encoded_byte
    
    #Method used to encode release mechanism flags into a single byte
    def encode_release_mech_flags(self):
        """
        PURPOSE: Encodes the release mechanism state flags as a single C Character Byte represented as a Python String
        INPUTS: NONE
        OUTPUTS: encoded_byte = The release mechanism flags encoded as a single Byte represented as a Python String
        """
        encoded_byte = 0
        num_flags = len(self.release_mechanism_states) - 1
        
        #Converting the flags list into an Integer containing the Flags in the Same Order [0, 1, 1] ==> 011
        for index, stabilisation_flag in enumerate(self.release_mechanism_states):
            index = num_flags - index
            encoded_byte |= (stabilisation_flag << index)
        
        #Packing the Python Integer into a C Char
        encoded_byte = ctb.char_pack(encoded_byte)
        return encoded_byte
    
    #Method used to encode the lifting bag inflation mechanism state
    def encode_inflate_mech_state(self):
        """
        PURPOSE: Encodes the inflation mechanism state into a single C Character Byte represented as a Python String
        INPUTS: NONE
        OUTPUTS: encoded_byte = The inflation mechanism state as a single Byte represnted as a Python String
        """
        encoded_byte = ctb.char_pack(self.inflate_mechanism_state)
        return encoded_byte
    
    #Method used to encode the position of the grabbing mechanism
    def encode_grabber_position(self):
        """
        PURPOSE: Encodes the grabber position into a single C Character Byte represented as a Python String
        INPUTS: NONE
        OUTPUTS: encoded_byte = The grabber position as a single Byte represented as a Python String
        """
        encoded_byte = ctb.char_pack(self.grabber_val)
        return encoded_byte
    
    #Method used to encode the levelling motor flag
    def encode_levelling_motor_flag(self):
        """
        PURPOSE: Encodes the levelling motor rotation direction and speed as a single C Character Byte represented as a Python String
        INPUTS: NONE
        OUTPUTS: encoded_byte = The levelling motor rotation and speed as a single Byte represented as a Python String
        """
        encoded_byte = ctb.char_pack(self.levelling_motor_flag)
        return encoded_byte
    
    #Method used to encode a camera channel index
    def encode_camera_index(self, camera_index):
        """
        PURPOSE: Encodes the camera index as a single C Character Byte represented as a Python String
        INPUTS: camera_index = The camera index to be encoded
        OUTPUTS: encoded_byte = The camera index as a single Byte represented as a Python String
        """
        encoded_byte = ctb.char_pack(camera_index)
        return encoded_byte
    
    #DECODING FUNCTIONS
    #Method used to decode the ROV IMU values
    def decode_imu_vals(self, encoded_message):
        """
        PURPOSE: Decodes the ROV IMU values from the recieved message from the ROV
        INPUTS: encoded_message = The ROV IMU Values as an encoded String
        OUTPUTS: NONE
        """
        index = 0
        
        #Decoding the individual IMU values and storing them in the IMU Vals List
        for imu_val_index in range(0, len(self.imu_vals)):
            raw_encoded_value = encoded_message[index : index + 4]
            self.imu_vals[imu_val_index] = ctb.float_unpack(raw_encoded_value)
            index += 4
    
    #INPUT METHOODS - TO BE USED BY THE SOFTWARE TEAM TO SEND VALUES TO THE ROV
    #Method used to set all of the ROV's Thruster Values at once
    def set_thrusts(self, new_thrust_vals):
        """
        PURPOSE: Sets the current thruster values of the ROV
        INPUTS: new_thrust_vals = A list of the new thrust values as integers
        OUTPUTS: NONE
        """
        self.thrust_vals = new_thrust_vals
    
    #Method used to set an individual ROV Thruster Value
    def set_thrust(self, new_thrust, thruster_index):
        """
        PURPOSE: Sets the current thruster values of a specific ROV thruster
        INPUTS: new_thrust = The new thrust value of the ROV thruster
                thruster_index = The index of the thruster to set the thrust value for
        OUTPUTS: NONE
        """
        self.thrust_vals[thruster_index] = new_thrust
    
    #Method used to set an axis stabilisation flag
    def set_axis_stable(self, stabilisation_flag, axis_index):
        """
        PURPOSE: Enables or disables the stabilisation of a given axis
        INPUTS: stabilisation_flag = An integer value that enables or disabled axis stabilisation. 1 = Enable, 0 = Disable
                axis_index = The index of the axis to set the stabilisation for
        OUTPUTS: NONE
        """
        self.axis_stabilisation_flags[axis_index] = stabilisation_flag
    
    #Method used to set the state of a lifting bag release mechanism
    def set_lift_bag_release(self, mech_state, mech_index):
        """
        PURPOSE: Enables or disables the release mechanism of a defined lifting bag
        INPUTS: mech_state = Enables or disables the release mechanism. 1 = Enabled (Open), 0 = Disabled (Closed)
                mech_index = The index of the mechanism being set as an integer
        OUTPUTS: NONE
        """
        self.release_mechanism_states[mech_index] = mech_state

    #Method used to set the state of a lifting bag release mechanism
    def set_lift_bag_EM_release(self, mech_state, mech_index):
        """
        PURPOSE: Enables or disables the EM releaseof a defined lifting bag
        INPUTS: EM_mech_state = Enables or disables the EM release mechanism. 1 = Enabled (Open), 0 = Disabled (Closed)
                EM_mech_index = The index of the mechanism being set as an integer
        OUTPUTS: NONE
        """
        self.EM_release_mechanism_states[EM_mech_index] = EM_mech_state

        
    #Method used to set the state of the lifting bag inflation mechanism
    def set_lift_bag_inflate(self, inflate_mech_state):
        """
        PURPOSE: Enables or disables the lifting bag inflation mechanism.
        INPUTS: inflate_mech_state = 1 = Inflation Mechanism Active, 0 = Inflation Mechanism Disabled
        OUTPUTS: NONE
        """
        self.inflate_mechanism_state = inflate_mech_state
    
    #Method used to set the grabber arm manipulator position
    def set_grabber_position(self, grabber_position):
        """
        PURPOSE: Sets the position of the grabber arm as a percentage open
        INPUTS: grabber_position = The position of the grabber as a percentage open. 100 = Fully Open, 0 = Fully Closed
        OUTPUTS: NONE
        """
        self.grabber_val = grabber_position
    
    #Method used to set the levelling motor rotation speed and direction
    def set_levelling_motor_rotation(self, levelling_motor_val):
        """
        PURPOSE: Sets the direction and speed of the levelling motors rotation
        INPUTS: levelling_motor_val = An integer value representing the direction and speed of the motors rotation. 200 = Rotate full speed Clockwise, 0 = Rotate full speed Anticlockwide, 100 = Full Stop
        OUTPUTS: NONE        
        """
        self.levelling_motor_flag = levelling_motor_val
    
    #Method used to set the currently selected cameras for channels 1 and 2
    def set_selected_cameras(self, camera_one_index, camera_two_index):
        """
        PURPOSE: Sets the selected cameras for camera feeds one and two
        INPUTS: camera_one_index = An integer value of 0 - 5 that selects the camera shown on channel 1
                camera_two_index = An integer value of 0 - 5 that selects the camera shown on channel 2
        OUTPUTS: NONE
        """
        self.camera_one_index = [camera_one_index]
        self.camera_two_index = [camera_two_index]
    
    #OUTPUT METHODS - TO BE USED BY THE SOFTWARE TEAM TO RECIEVE VALUES FROM THE ROV
    #Method used to get the current IMU values
    def get_imu(self):
        """
        PURPOSE: Gets the current values outputted by the ROV IMU
        INPUTS: NONE
        OUTPUTS: imu_vals = The current values from the IMU as a list of floats
        """
        return self.imu_vals
    
    #Method used to get the ROVs current Depth
    def get_depth(self):
        """
        PURPOSE: Gets the current depth of the ROV in meters compared to the waters surface
        INPUTS: NONE
        OUTPUTS: depth_current = The current depth of the ROV as a float
        """
        return self.depth_current
    
    #Method used to get the Platform IMUs Angles to the Horizontal
    def get_platform_imu(self):
        """
        PURPOSE: Gets the current angles to the horizontal in the X and Y Direction for the platform IMU.
        INPUTS: NONE
        OUTPUTS: x_angle = The angle to the horizontal in the X direction
                y_angle = The angle to the horizontal in the Y direction
        """
        x_angle = self.platform_imu_vals[0]
        y_angle = self.platform_imu_vals[1]
        return x_angle, y_angle


# -*- coding: utf-8 -*-
"""
This code converts Python Values into Binary C Constructs represented as Python Strings. Specifically this version of the module is used for networking
purposes and thus uses the networking formatting character ==> "!".

RELEASE DATE: ENTER RELEASE DATE HERE
RELEASE VERSION: ENTER RELEASE VERSION HERE
AUTHOR: Sam Maxwell
"""
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
#MODULES
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
import struct        #Handles the packing of Binary Values into Strings that represent C Structures as well as the unpacking of the Strings into Binary Values

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
#DEFINITIONS
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
CHR_FMT_STR = "!B"
SHRT_FMT_STR = "!h"
INT_FMT_STR = "!i"
LONG_FMT_STR = "!l"
FLOAT_FMT_STR = "!f"
DBLE_FMT_STR = "!d"

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
#FUNCTIONS
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
#PACKING FUNCTIONS
#Function used to convert a Python Integer into a C Char
def char_pack(unpacked_val):
    #Ensuring that the Python value is an Integer
    unpacked_val = int(unpacked_val)
    
    #Ensuring that the Python Value is less than 256 and thus can be converted into a Character
    assert unpacked_val < 256
    
    #Packing the Integer into a string representing a C Char
    packed_val = struct.pack(CHR_FMT_STR, unpacked_val)
    return packed_val

#Function used to convert a Python Integer to a C Short
def short_pack(unpacked_val):
    #Ensuring the Python Value is an Integer
    unpacked_val = int(unpacked_val)
    
    #Packing the Integer into a string representing a C Short
    packed_val = struct.pack(SHRT_FMT_STR, unpacked_val)
    return packed_val

#Function used to convert a Python Integer to a C Integer
def int_pack(unpacked_val):
    #Ensuring the Python Value is an Integer
    unpacked_val = int(unpacked_val)
    
    #Packing the Integer into a string representing a C Integer
    packed_val = struct.pack(INT_FMT_STR, unpacked_val)
    return packed_val

#Function used to convert a Python Long to a C Long
def long_pack(unpacked_val):
    #Ensuring that the Python Value is an Integer
    unpacked_val = int(unpacked_val)
    
    #Packing the Integer into a string representing a C Long
    packed_val = struct.pack(LONG_FMT_STR, unpacked_val)
    return packed_val

#Function used to convert a Python Float to a C Float
def float_pack(unpacked_val):
    #Ensuring that the Python Value is a Float
    unpacked_val = float(unpacked_val)
    
    #Packing the Float into a string representing a C Float
    packed_val = struct.pack(FLOAT_FMT_STR, unpacked_val)
    return packed_val

#Function used to convert a Python Float to a C Double
def double_pack(unpacked_val):
    #Ensuring that the Python Value is a Float
    unpacked_val = float(unpacked_val)
    
    #Packing the Float into a string representing a C Double
    packed_val = struct.pack(DBLE_FMT_STR, unpacked_val)
    return packed_val

#UNPACKING FUNCTIONS
#Function used to convert a C Char to a Python Integer
def char_unpack(packed_val):
    #Unpacking the C Char
    unpacked_val = struct.unpack(CHR_FMT_STR, packed_val)
    unpacked_val = unpacked_val[0]
    return unpacked_val

#Function used to convert a C Short to a Python Integer
def short_unpack(packed_val):
    #Unpacking the C Short
    unpacked_val = struct.unpack(SHRT_FMT_STR, packed_val.encode())
    unpacked_val = unpacked_val[0]
    return unpacked_val

#Function used to convert a C Integer to a Python Integer
def int_unpack(packed_val):
    #Unpacking the C Integer
    unpacked_val = struct.unpack(INT_FMT_STR, packed_val)
    unpacked_val = unpacked_val[0]
    return unpacked_val

#Function used to convert a C Long to a Python Long
def long_unpack(packed_val):
    #Unpacking the C Long
    unpacked_val = struct.unpack(LONG_FMT_STR, packed_val)
    unpacked_val = unpacked_val[0]
    return unpacked_val

#Function used to convert a C Float to a Python Float
def float_unpack(packed_val):
    #Unpacking the C Float
    unpacked_val = struct.unpack(FLOAT_FMT_STR, packed_val)
    unpacked_val = unpacked_val[0]
    return unpacked_val

#Function used to convert a C Double to a Python Float
def double_unpack(packed_val):
    #Unpacking the C Double
    unpacked_val = struct.unpack(DBLE_FMT_STR, packed_val)
    unpacked_val = unpacked_val[0]
    return unpacked_val
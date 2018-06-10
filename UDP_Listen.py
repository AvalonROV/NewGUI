#This is a simple code to recieve and print messages over a UDP server

import converttobinary as ctb    #Module that handles conversion of Python Values to Binary
import socket
import struct

HOST="localhost"
PORT=8000

s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

s.bind((HOST,PORT))#Binding togther two sets of data

#print(buff[3])
#print(buff.encode())

#x = ctb.short_unpack()
while True:
    buff = s.recv(50)
    print(buff) # Receives 30 bits as character that much long

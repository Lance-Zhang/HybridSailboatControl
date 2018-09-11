# -*- coding: utf-8 -*-
"""
Created on Mon May 14 16:18:14 2018

@author: fahad

@contributor: Lianxin Zhang
"""

import socket
import sys
import time
import tty, termios


#-------------Initialization-----------------------------------
def tcpPC():
    # this is the tcp client to connect with sailboat server
    TCP_IP = '192.168.31.148'
    TCP_PORT = 50007
    BUFFER_SIZE = 1024
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Client socket1 is created \n')
    try:
        s.connect((TCP_IP, TCP_PORT))
        print(' TCP1 Connected \n')
    except:
        print('An Error Occured! \n')
        sys.exit()
      
    s.sendall('Hello'.encode('utf-8')) ## Converting into Bytes
    time.sleep(0.2) ## 0.2 second delay
    
    
    #-------------------Sending Commands ----------------------------  
    print('****************Manual Control Mode********************\n\
Please Enter W for Forward, A for Turning left, D for Turning right,\n\
S for Stop, Q for Quit to choose other modes.')
    while True:
        fd=sys.stdin.fileno()
        old_settings=termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            command=sys.stdin.read(1).upper()
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            
        if command == 'S' or command == 'W' or command == 'A' or command == 'D':
            message_bytes = command.encode('utf-8') ## Converting into Bytes
            s.sendall(message_bytes)
        elif command == 'Q':
            answer = raw_input('Quit the Manual Control System. Are you sure? Y/N ').upper()
            if answer == 'Y':
                s.sendall(command.encode('utf-8'))
                break
            elif answer == 'N':
                print('Reinput please.')
                continue
            break
        elif command == '':
            pass
        else:
            print('Wrong input: not B, P or E. Retype please.')
            continue

        # time.sleep(0.2) ## 0.2 second pause
    
    data = s.recv(BUFFER_SIZE)
    print (data.decode('utf-8'))
    s.close()
    time.sleep(0.5) ## 0.5 second delay
    print('TCP1 Communication Closed') 
    sys.exit()

#----------------------------------------------------------------

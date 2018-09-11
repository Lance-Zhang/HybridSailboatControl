# -*- coding: utf-8 -*-
"""
Created on Mon May 14 22:05:43 2018

@author: fahad

@contributor: Lianxin Zhang

This is the main actuator to control the propellers
"""


import time
import os
import pigpio
import globalvar as gl
os.system('sudo killall -9 pigpiod')
os.system('sudo pigpiod')
time.sleep(1)

#-------------Receiving Commands-----------------
def sailing(conn):
    
    #-----------ESC Configuration----------------------
    ESC1 = 4 # Motor1
    ESC2 = 17 # Motor2
    ESC3 = 24 # Rudders
    ESC4 = 25 # Sails

    STBY = 23
    AIN2 = 21 # For motor direction
    AIN1 = 20 # For motor direction
    BIN1 = 27 # For motor direction
    BIN2 = 22 # For motor direction
    
    BUFFER_SIZE = 1024 # For TCP receiver
    #--------------------------------------------------
    
    gl.set_value('flag',False)
    angle = 1300 # Rudder Straight
    
    pi = pigpio.pi()
    pi.set_mode(STBY, pigpio.OUTPUT) # Setting GPIO 23 as OUTPUT
    pi.set_mode(AIN1, pigpio.OUTPUT)
    pi.set_mode(AIN2, pigpio.OUTPUT)
    pi.set_mode(BIN1, pigpio.OUTPUT)
    pi.set_mode(BIN2, pigpio.OUTPUT)
    pi.write(STBY,1) # Turining GPIO 23 High
    
    while True:
        data = conn.recv(BUFFER_SIZE)
        ReceivedData = str(data.decode('utf-8'))
        
        if ReceivedData.upper() == "Q":
            gl.set_value('flag',True)
            print('Quit from the Manual Control Mode')
            break
        elif ReceivedData.upper() == "W":
            print('Moving Forward')
            pi.set_servo_pulsewidth(ESC3,angle)
            pi.set_servo_pulsewidth(ESC4,900) # Sails Tighten
            pi.write(AIN1,1) # Turining GPIO 20 Low
            pi.write(AIN2,0) # Turining GPIO 21 High
            pi.write(BIN1,1) # Turining GPIO 27 Low
            pi.write(BIN2,0) # Turining GPIO 22 High
            PWM1 = 255
            PWM2 = 200
        elif  ReceivedData.upper() == "S":
            print('Stopped')
            PWM1 = 0
            PWM2 = 0
            pi.set_servo_pulsewidth(ESC3,angle)
            pi.set_servo_pulsewidth(ESC4,900)
        elif  ReceivedData.upper() == "A":
            print('Turning Left')
            pi.set_servo_pulsewidth(ESC3,800)
            pi.set_servo_pulsewidth(ESC4,1700) # Sails Loosen
            pi.write(AIN1,1) # Turining GPIO 20 Low
            pi.write(AIN2,0) # Turining GPIO 21 High
            pi.write(BIN1,0) # Turining GPIO 27 Low
            pi.write(BIN2,1) # Turining GPIO 22 High
            PWM1 = 255
            PWM2 = 220
        elif  ReceivedData.upper() == "D":
            print('Turning Right')
            pi.set_servo_pulsewidth(ESC4,1700) # Sails Loosen
            pi.set_servo_pulsewidth(ESC3,1700)
            pi.write(AIN1,0) # Turining GPIO 20 Low
            pi.write(AIN2,1) # Turining GPIO 21 High
            pi.write(BIN1,1) # Turining GPIO 27 Low
            pi.write(BIN2,0) # Turining GPIO 22 High
            PWM1 = 220
            PWM2 = 255
        else:
            PWM1 = 0
            PWM2 = 0
            pi.set_servo_pulsewidth(ESC3,angle) # Rudder Straight
            pi.set_servo_pulsewidth(ESC4,900) # Sails Tighten

        gl.set_value('PWM1',PWM1) # PWM for Motor1
        gl.set_value('PWM2',PWM2) # PWM for Motor2
        pi.set_PWM_dutycycle(ESC1, PWM1)
        pi.set_PWM_dutycycle(ESC2, PWM2)
        time.sleep(0.5)
    
    # End the program        
    pi.set_PWM_dutycycle(ESC1, 0)
    pi.set_PWM_dutycycle(ESC2, 0)
    pi.set_servo_pulsewidth(ESC3,angle) # Rudder Straight
    pi.set_servo_pulsewidth(ESC4,900) # Sails Tighten
    print('Motors Stopped \n')
    time.sleep(0.4)
    pi.stop()
    time.sleep(0.5)

    
#    conn.close()
#    time.sleep(1)
#    print('Connection closed!')

#------------------------------------------------

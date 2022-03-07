#!/usr/bin/python

# Writes some text to a Serial port, toggles RS485 send/receive and then reads back the results
# Make sure to use the correct Serial port for your computer for this to work
# based on https://github.com/trevhoot/BestBuds/blob/master/python/serialcode.py

import RPi.GPIO as GPIO
import time
import serial

RW_PIN = 18
MODE_SEND = 1
MODE_RECEIVE = 0

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(RW_PIN,GPIO.OUT)

# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial(
    port='/dev/ttyAMA1',
    baudrate=9600,
    parity=serial.PARITY_ODD,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=5
)

GPIO.output(RW_PIN,MODE_RECEIVE)

ser.isOpen()

print 'Type command:'

while 1 :
    # get keyboard input
    input = raw_input(">> ")
        # Python 3 users
        # input = input(">> ")
    if input == 'exit':
        ser.close()
        exit()
    else:
        GPIO.output(RW_PIN,MODE_SEND)
        # send the input to the device
        ser.write(input + '\r\n')
        # force sending right away
        time.sleep(0.1)
        ser.flush()
        out = ''
        GPIO.output(RW_PIN,MODE_RECEIVE)
        # let's wait one second before reading output (let's give device time to answer)
        time.sleep(0.1)
        
    while ser.inWaiting() > 0:
        out += ser.read(1)
    if out != '':
        print ">>" + out

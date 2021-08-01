#!/usr/bin/env python3
#
# Author: Dick Carrillo 2021
# All rights reserved.
#
#
# This code is licensed under standard 3-clause BSD license.
# See file LICENSE supplied with this package for the full license text.

#import numpy as np
import sys
import signal
from datetime import datetime, timedelta
from time import sleep
from subprocess import Popen, PIPE
from os import makedirs
from os.path import isdir, isfile, join
from ntpath import dirname, basename
import os
import socket
import time


ipLocal = str(sys.argv[1])
portaLocal = int(sys.argv[2])
idDevice = str(sys.argv[3])
#SOCKET FEATURE:
s = socket.socket()
s.connect((ipLocal,portaLocal))

def get_rf_info():
 # This Hard solution run a shell script that already has access to the embbedded system
 # It save the output in a file rf_raw_info.txt
 os.system('./scrip.sh | grep = > rf_raw_info.txt')


def reading_file(outputfile):
 # we open a file and create the vector information
 info_data = ''
 counter = 0
 info_data = idDevice
 with open(outputfile, encoding='utf-8', errors='ignore') as inputfile:
    for line in inputfile:
        counter = counter + 1
        if counter < 5:
             tmp_lst = line.strip().split('=')
             data = (tmp_lst[1]);
             #info_data.append([data])
        elif counter == 5:
             print('Do nothing ...')
             data = ''
        else:
             tmp_lst = line.strip().split('=')
             date1 = (tmp_lst[1])
             #date2 = tmp_lst[2]
             #date3 = tmp_lst[3]
             #date4 = tmp_lst[4]
             #date5 = tmp_lst[5]
             #date6 = tmp_lst[6]
             #date.append([date1, date2, date3, date4, date5, date6])
             data = date1

        #info_data.append([ data ])
        info_data = info_data + ' ' +  data


 if not info_data:
        raise ValueError('Nothing reached the server.')

 #iinfo_data = np.array(info_data)

 return info_data

def transmitting(info):
    s = socket.socket()
    s.connect(('100.100.100.10',12345))
    print('transmitting data ..')
    s.send(info.encode());
    info = 'bye'
    s.send(info.encode());
    s.close()

def keyboardInterruptHandler(signal, frame):
    print("KeyboardInterrupt (ID: {}) has been caught. Cleaning up...".format(signal))
    info = 'Bye'
    s.send(info.encode())
    s.close()
    print('INTERRUPTION is ON')
    exit(0)

signal.signal(signal.SIGINT, keyboardInterruptHandler)

#MAIN LOOP
flag = 0
while True:
            get_rf_info()
            print('info was created...')
            outputinfo = reading_file('rf_raw_info.txt')
            outf = str(outputinfo)
            print(outf)
            s.send(outf.encode())
            with  open('coringa.txt', encoding='utf-8', errors='ignore') as inputfile:
                for lineinfo in inputfile:
                    if lineinfo[0] == 'B':
                        flag = 1
            if flag > 0: #TO CHECK SIGNAL TO STOP TRANSMITTION
                info = 'Bye'
                s.send(info.encode())
                s.close()
                break
s.close()


#!/usr/bin/python3

from __future__ import print_function

from client import ClientProtocol
from server import Server
from composable_paxos import *
from master_strategy import *
from messenger import *
from replicated_value import *
from resolution_strategy import *
from sync_strategy import *
import config
import serial
import time
import smbus
import csv
import os


def createData(self):
	
	DEVICE_BUS = 1
	DEVICE_ADDR = 0x17

	TEMP_REG = 0x01
	LIGHT_REG_L = 0x02
	LIGHT_REG_H = 0x03
	STATUS_REG = 0x04
	ON_BOARD_TEMP_REG = 0x05
	ON_BOARD_HUMIDITY_REG = 0x06
	ON_BOARD_SENSOR_ERROR = 0x07
	BMP280_TEMP_REG = 0x08
	BMP280_PRESSURE_REG_L = 0x09
	BMP280_PRESSURE_REG_M = 0x0A
	BMP280_PRESSURE_REG_H = 0x0B
	BMP280_STATUS = 0x0C
	HUMAN_DETECT = 0x0D

	bus = smbus.SMBus(DEVICE_BUS)

	aReceiveBuf = []

	aReceiveBuf.append(0x00)

	for i in range(TEMP_REG,HUMAN_DETECT + 1):
		aReceiveBuf.append(bus.read_byte_data(DEVICE_ADDR, i))

	#return str(aReceiveBuf[TEMP_REG]), str((aReceiveBuf[LIGHT_REG_H] << 8 | aReceiveBuf[LIGHT_REG_L])), str(aReceiveBuf[ON_BOARD_HUMIDITY_REG]), str((aReceiveBuf[BMP280_PRESSURE_REG_L] | aReceiveBuf[BMP280_PRESSURE_REG_M] << 8 | aReceiveBuf[BMP280_PRESSURE_REG_H] << 16))
	return aReceiveBuf[TEMP_REG], (aReceiveBuf[LIGHT_REG_H] << 8 | aReceiveBuf[LIGHT_REG_L]), aReceiveBuf[ON_BOARD_HUMIDITY_REG], aReceiveBuf[ON_BOARD_TEMP_REG]
        

def main():
	#declare node name
    node = 1
    filename = 'sensor-1_data_raft.csv'
    #initialize Server obj
	serv = Server(node)
    #set serial connection with ESP32
    s = serial.Serial('/dev/ttyS0', 115200)
    #initialize packet counter
    count = 1
	#node counter
	counter = 1
    #declare header for csv file
    header = ['nodeName', 'packetNumber', 'temperature', 'brightness', 'humidity', 'onBoardTemp']  
   
    #create csv file
    with open(filename, 'w', encoding='UTF8', newline='') as f:
        #writer object
        writer = csv.writer(f)
        #write the header to the csv file
        writer.writerow(header)
        #loop 
        while count <= 1000:
		    #2 sec interval
            time.sleep(2)
            #check if this node is master node			 
            if serv.get_master() == node:
                if counter <= 3:
                    #increment counter				
                    counter+=1
					#initialize Client object and propose new value
					ClientProtocol(node, counter)
                else:
				    #restart counter
                    counter = 1
					#initialize Client object and propose new value
					ClientProtocol(node, counter)
			#if the value of the counter matches node number, sent packet		
            if counter == node:
                #read sensor hub data
                temp, light, humidity, onBoardTemp = o.createData()
                #write data to csv file
                data = [node, count, temp, light, humidity, onBoardTemp]
                writer.writerow(data)
                #send packet over lora
                s.write(b'%d,%d,%d,%d,%d,%d' % (node, count, temp, light, humidity, onBoardTemp)) 
                #print("COUNTER: %d" % o.getCounter())
            #increment packet count
            count+=1
        f.flush()
        f.close()


if __name__ == '__main__':
    main()
    os.system('sudo poweroff')


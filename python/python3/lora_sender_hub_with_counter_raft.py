#!/usr/bin/python3

from __future__ import print_function

from pysyncobj import *
import serial
import time
import smbus
import csv
import os

class RaftObj(SyncObj):

    def __init__(self, selfNode, otherNodes):
        super(TestObj, self).__init__(selfNode,otherNodes)
        self.__counter = 1


    @replicated
    def setCounter(self, value):
        self.__counter = value		
        return self.__counter


    @replicated
    def addValue(self, value):
        self.__counter += value
        return self.__counter


    def getCounter(self):
        return self.__counter
        
        
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
    my_ip = "192.168.1.1"
    o = RaftObj('192.168.1.1:12345', ['192.168.1.2:12345', '192.168.1.3:12345'])
    old_value = -1
    filename = 'sensor-1_data_raft.csv'
    #set serial connection with ESP32
    s = serial.Serial('/dev/ttyS0', 115200)
    #declare node name
    node = 1
    #initialize packet counter
    count = 1
    #temp, light, humidity, onBoardTemp = createData()
    #print(node, count, temp, light, humidity, pressure)
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
            time.sleep(2)        
            if o.getCounter() != old_value:
                old_value = o.getCounter()
            if str(o._getLeader()).split(":", 1)[0] == my_ip:
                if o.getCounter() <= 3: 
                    o.addValue(1)
                else:
                    o.setCounter(1)
            if o.getCounter() == node:
                #read sensor hub data
                temp, light, humidity, onBoardTemp = o.createData()
                #write data to csv file
                data = [node, count, temp, light, humidity, onBoardTemp]
                writer.writerow(data)
                #send packet over lora
                s.write(b'%d,%d,%d,%d,%d,%d' % (node, count, temp, light, humidity, onBoardTemp)) 
                #print("COUNTER: %d" % o.getCounter())
            
            count+=1
        f.flush()
        f.close()


if __name__ == '__main__':
    main()
    os.system('sudo poweroff')


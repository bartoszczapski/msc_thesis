#!/usr/bin/python3
import serial
import time
import smbus
import csv

def createData():
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
    #set UART serial connection with ESP32
    s = serial.Serial('/dev/ttyS0', 115200)
    #declare node name
    node = 4
    #initialize packet counter
    count = 1
    #temp, light, humidity, onBoardTemp = createData()
    #print(node, count, temp, light, humidity, pressure)
    #declare header for csv file
    header = ['nodeName', 'packetNumber', 'temperature', 'brightness', 'humidity', 'onBoardTemp']  
   
    #create csv file
    with open('sensor-4_data.csv', 'w', encoding='UTF8', newline='') as f:
        #writer object
        writer = csv.writer(f)
        #write the header to the csv file
        writer.writerow(header)

        #loop 
        while True:        
            #read sensor hub data
            temp, light, humidity, onBoardTemp = createData()
            #write data to csv file
            data = [node, count, temp, light, humidity, onBoardTemp]
            #send packet over lora
            s.write(b'%d,%d,%d,%d,%d,%d' % (node, count, temp, light, humidity, onBoardTemp))
            #save packet to the csv file
			writer.writerow(data)			
            print(count)
            count += 1
            time.sleep(2)


if __name__ == '__main__':
    main()


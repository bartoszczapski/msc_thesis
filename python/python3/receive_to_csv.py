#!/usr/bin/python3
import re
import serial
import csv
#set serial connection with ESP32
s=serial.Serial('/dev/ttyS0',115200)
#exclude pattern
pattern = "free"
#declare header for csv file
header = ['nodeName', 'packetNumber', 'temperature', 'brightness', 'humidity', 'onBoardTemp']
#create csv file
with open('/home/bart/msc_python/data.csv', 'w', encoding='UTF8') as f:
    #writer object
    writer = csv.writer(f)
	#write the header to the csv file
    writer.writerow(header)
	#loop
    while True:
	    #read input from UART
        data = s.readline()
		#do not process if pattern exists
        if data and not re.search(pattern, data.decode()):
		    #decode from bytestream
            d = data.decode()
			#cleanup
            final_data = d.replace('"','').replace("b","").replace("'", "").replace("\r","").replace("\n","").replace("-",",").replace(" ","")
            #write data to the file
			writer.writerow(final_data.split(",")) 
           

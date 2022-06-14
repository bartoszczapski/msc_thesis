from LoRaSender import Sender
import LoRaReceiver
from machine import UART
import network
import time
import ntptime
from config import *
from machine import Pin, SPI
from sx127x import SX127x

wlan = network.WLAN(network.STA_IF)
wlan.active(True)


wlan.connect('*********', '*********')
#time.sleep(1)


while not wlan.isconnected():    
    time.sleep(2)



print(wlan.ifconfig())
ntptime.settime()
time.sleep(2)
device_spi = SPI(baudrate = 115200, 
        polarity = 0, phase = 0, bits = 8, firstbit = SPI.MSB,
        sck = Pin(device_config['sck'], Pin.OUT, Pin.PULL_DOWN),
        mosi = Pin(device_config['mosi'], Pin.OUT, Pin.PULL_UP),
        miso = Pin(device_config['miso'], Pin.IN, Pin.PULL_UP))

lora = SX127x(device_spi, pins=device_config, parameters=lora_parameters)


LoRaReceiver.receive(lora)
uart = UART(2, 115200)
uart.init(115200, bits=8, parity=None, stop=1, tx=17, rx=13)

print(time.localtime())




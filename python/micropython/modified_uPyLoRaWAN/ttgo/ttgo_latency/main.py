from LoRaSender import Sender
from LoRaReceiver import Receiver
from machine import UART
import network
import time
import ntptime
from config import *
from machine import Pin, SPI
from sx127x import SX127x

wlan = network.WLAN(network.STA_IF)
wlan.active(True)


wlan.connect('VM9273060', '58RXkuyabvdn')
#time.sleep(1)


while not wlan.isconnected():    
    time.sleep(2)



print(wlan.ifconfig())
time.sleep(2)
ntptime.settime()
#time.sleep(2)
device_spi = SPI(baudrate = 115200, 
        polarity = 0, phase = 0, bits = 8, firstbit = SPI.MSB,
        sck = Pin(device_config['sck'], Pin.OUT, Pin.PULL_DOWN),
        mosi = Pin(device_config['mosi'], Pin.OUT, Pin.PULL_UP),
        miso = Pin(device_config['miso'], Pin.IN, Pin.PULL_UP))

lora = SX127x(device_spi, pins=device_config, parameters=lora_parameters)


sender = Sender(lora)
uart = UART(2, 115200)
uart.init(115200, bits=8, parity=None, stop=1, tx=17, rx=13)

print(time.localtime())
while True:
    msg = uart.readline()
    if msg:
        n = time.time_ns() // 1000000
        sender.send(msg, n)



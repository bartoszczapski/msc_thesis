from LoRaSender import Sender
import LoRaReceiver
from machine import UART

from config import *
from machine import Pin, SPI
from sx127x import SX127x

device_spi = SPI(baudrate = 115200, 
        polarity = 0, phase = 0, bits = 8, firstbit = SPI.MSB,
        sck = Pin(device_config['sck'], Pin.OUT, Pin.PULL_DOWN),
        mosi = Pin(device_config['mosi'], Pin.OUT, Pin.PULL_UP),
        miso = Pin(device_config['miso'], Pin.IN, Pin.PULL_UP))

lora = SX127x(device_spi, pins=device_config, parameters=lora_parameters)

sender = Sender(lora)
uart = UART(2, 115200)
uart.init(115200, bits=8, parity=None, stop=1, tx=17, rx=13)
while True:
    msg = uart.readline()
    if msg:
        sender.send(msg)


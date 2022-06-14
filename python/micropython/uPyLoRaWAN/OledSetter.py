from machine import Pin, I2C
import ssd1306
import time

def setOled():
    # Heltec LoRa 32 with OLED Display
    oled_width = 128
    oled_height = 64
    # OLED reset pin
    i2c_rst = Pin(16, Pin.OUT)
    # Initialize the OLED display
    i2c_rst.value(0)
    time.sleep_ms(5)
    i2c_rst.value(1) # must be held high after initialization
    # Setup the I2C lines
    i2c_scl = Pin(15, Pin.OUT, Pin.PULL_UP)
    i2c_sda = Pin(4, Pin.OUT, Pin.PULL_UP)
    # Create the bus object
    i2c = I2C(scl=i2c_scl, sda=i2c_sda)
    # Create the display object
    oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)
    return oled

def displayOled(oled, role, count):
    oled.fill(0)
    #oled.text(wlan.ifconfig()[0], 0, 0)
    oled.text(str(role), 0, 25)
    oled.text(str(count), 0, 55)
    #oled.line(0, 0, 50, 25, 1)
    oled.show()


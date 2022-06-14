import OledSetter
from ssd1306_i2c import Display
import ssd1306
import time


def receive(lora):
    print("LoRa Receiver")
    oled = OledSetter.setOled()
    role = "RECEIVER"
    while True:
        if lora.received_packet():
            lora.blink_led()
            payload = lora.read_payload()
            print(payload)
            OledSetter.displayOled(oled, role, payload)

import OledSetter
from ssd1306_i2c import Display
import ssd1306
import time

class Receiver:
    def __init__(self, lora):
        self.lora = lora

	def receive(lora):
		print("LoRa Receiver")
		oled = OledSetter.setOled()
		role = "RECEIVER"
		while True:
			if lora.received_packet():
				n = time.time_ns() // 1000000
				lora.blink_led()
				p = lora.read_payload()
				payload = '{m} - {i}'.format(m=p, i=n)
				
				print(payload)
				OledSetter.displayOled(oled, role, payload)

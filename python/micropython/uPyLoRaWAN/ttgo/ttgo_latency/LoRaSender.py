import OledSetter
import time

class Sender:
    def __init__(self, lora):
        self.lora = lora
       


    def send(self, msg, n):
        self.lora.blink_led()
        print("LoRa Sender")
        oled = OledSetter.setOled()
    
        role = "TRANSMITTER"
        payload = '{p} - {i}'.format(p=msg, i=n)
        print("Sending packet: \n{}\n".format(payload))
        OledSetter.displayOled(oled, role, payload)
        
        self.lora.println(payload)
        #self.lora.println(n)
    
    

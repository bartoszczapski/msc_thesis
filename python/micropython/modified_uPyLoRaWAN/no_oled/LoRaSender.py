#import OledSetter

class Sender:
    def __init__(self, lora):
        self.lora = lora
       


    def send(self, msg):
        self.lora.blink_led()
        print("LoRa Sender")
        #oled = OledSetter.setOled()
    
        role = "TRANSMITTER"
        payload = '{p}'.format(p=msg)
        print("Sending packet: \n{}\n".format(payload))
        #OledSetter.displayOled(oled, role, payload)
        self.lora.println(payload)
    
    
    

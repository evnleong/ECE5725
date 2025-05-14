import RPi.GPIO as GPIO
from globals import plant_data

class MSensor():


    def __init__(self,pin):
        self.pin = pin 
        GPIO.setup(pin, GPIO.IN)
        GPIO.add_event_detect(pin, GPIO.BOTH, bouncetime=300)
        GPIO.add_event_callback(pin, detect_moisture)

#Update shared state
def detect_moisture(pin):
        if GPIO.input(pin): 
            plant_data['moisture'] = False
        else: #Moisture Detected
            plant_data['moisture'] = True 
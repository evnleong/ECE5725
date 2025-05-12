#Class Definition for Temp and Humidity Sensor
import Adafruit_DHT

class THSensor():

    def __init__(self,pin):
        # Temp + Humidity Sensor
        self.sensor = Adafruit_DHT.DHT11
        self.pin = pin 


    def update_ht(self):
        try:
            humidity, temperatureC = Adafruit_DHT.read_retry(self.sensor, self.pin)
            temperatureF = temperatureC * (9/5) + 32 
            return humidity,temperatureF
        finally:
            pass





import Adafruit_DHT



class THSensor():

    def __init__(self,pin):
        # Temp + Humidity Sensor
        self.sensor = Adafruit_DHT.DHT11
        self.pin = pin 


    def update_ht(self):
        try:
            
            humidity, temperatureC = Adafruit_DHT.read_retry(self.sensor, self.pin)
            if humidity is not None and temperatureC is not None:
                temperatureF = round(temperatureC * (9/5) + 32, 1) 
                return humidity,temperatureF
            else:
                return -1,-1
        finally:
            pass





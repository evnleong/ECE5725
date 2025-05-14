import RPi.GPIO as GPIO
import time



class PlantPump():
  def __init__(self,pin):
    self.state = False
    self.pin = pin
    GPIO.setup(pin,GPIO.OUT,initial = GPIO.HIGH)

  def pump_on(self):
    try:
      GPIO.output(self.pin, GPIO.LOW)
      self.state = True
      print("Pump on")
      time.sleep(0.5)
      GPIO.output(self.pin, GPIO.HIGH)
      print("Pump off")
    except:
      GPIO.cleanup()
      print("pump failure")


 

  # def pump_off(self):
  #   try:
  #     GPIO.output(self.pin,GPIO.LOW)
  #     print("Pump off")
  #   except: 
  #     GPIO.cleanup()


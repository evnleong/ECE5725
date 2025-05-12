#Class Definition for UV grow light 
import pigpio
import time


class GrowLight():
    # Connect to pigpio daemon

    def __init__(self,pin):
        pass
        self.pin = pin
        # self.pi = pigpio.pi()
        self.dutyCycle = 0
        # if not self.pi.connected:
        #     exit()
        # self.pi.set_mode(pin, pigpio.OUTPUT)
    # Set GPIO 17 as output

    def increaseDutyCycle(self):
        try:
            # pigpio PWM range is 0–255
            dC = self.dutyCycle
            if dC <= 75:
                self.dutyCycle += 25
                pwm_value = int((self.dutyCycle / 100.0) * 255)
                # self.pi.set_PWM_dutycycle(self.pin, pwm_value)
                print(f"Set duty cycle to {self.dutyCycle}%")

        finally:
            pass
            # Turn off PWM and cleanup
            # self.pi.set_PWM_dutycycle(self.pin, 0)
            # self.pi.stop()

    def decreaseDutyCycle(self):
        try: 
            dC = self.dutyCycle
            if (dC >= 25):
                self.dutyCycle -= 25
                pwm_value = int((self.dutyCycle / 100.0) * 255)
                # self.pi.set_PWM_dutycycle(self.pin, pwm_value)
                print(f"Set duty cycle to {self.dutyCycle}%")
                time.sleep(2)  # Keep each duty cycle for 2 seconds
        finally:
            pass



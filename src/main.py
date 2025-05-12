import pygame,pigame
from pygame.locals import *
import time,datetime
import os
import sys
import RPi.GPIO as GPIO
from threading import Thread
from camera import PlantCamera
from light import GrowLight
from thsensor import THSensor

# Environment Setup 
os.putenv('SDL_VIDEODRV','fbcon')
os.putenv('SDL_FBDEV', '/dev/fb0')
os.putenv('SDL_MOUSEDRV','dummy')
os.putenv('SDL_MOUSEDEV','/dev/null')
os.putenv('DISPLAY','')

# Setup GPIO for TFT 
GPIO.setmode(GPIO.BCM)   
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#Pump control pin
pumpPin = 21


#Colours 
WHITE = (255,255,255)
BLACK = (0,0,0)
LIGHT_GREEN = (132, 245, 115)
DARK_GREEN = (27, 117, 13)

pygame.init()
pitft= pigame.PiTft() # enable touchscreen
appWidth = 320
appHeight = 240

#Date & Time 
date = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')

font_big = pygame.font.Font(None, 35)
font_med = pygame.font.Font(None, 20)
font_sm = pygame.font.Font(None,15)
text_surface = font_sm.render("Live Camera", True, (DARK_GREEN))
text_surface2 = font_big.render("Welcome!", True, (DARK_GREEN))
text_surface3 = font_big.render("Temp:", True, (DARK_GREEN))
timestamp_text = font_sm.render(f"Date: {date} " , True, (DARK_GREEN))
 

screen = pygame.display.set_mode((appWidth, appHeight))

# camera = Picamera2()

code_run = True

try:
    plantCam = PlantCamera()

except:
    code_run= False

growLight = GrowLight(pin=20)
thSensor = THSensor(pin=16)


# Assets 

sun_icon = pygame.transform.scale(pygame.image.load(os.path.join('assets','sun.png')), (40,40))
temp_icon = pygame.transform.scale(pygame.image.load(os.path.join('assets','temp.png')), (50,50))
water_icon= pygame.transform.scale(pygame.image.load(os.path.join('assets','water.png')), (50,50))


# Callbacks

def button27(channel):
      growLight.increaseDutyCycle()

def button23(channel):
      growLight.decreaseDutyCycle()

def button22(channel):
      print("button22")

def button17(channel):
      print("button17")

# Add event listeners
GPIO.add_event_detect(27, GPIO.RISING, callback = button27, bouncetime =200)
GPIO.add_event_detect(23, GPIO.RISING, callback = button23, bouncetime =200)
GPIO.add_event_detect(22, GPIO.RISING, callback = button22, bouncetime =200)
GPIO.add_event_detect(17, GPIO.RISING, callback = button17, bouncetime =200)

menu_level_1 =  True
menu_level_2 = False
start_preview = False


def temphumidityThread():
    humidity,temperature = thSensor.update_ht()
    text_humidity = font_big.render(f"{humidity}%", True, (255, 255, 255))
    text_temperature = font_big.render(f"{temperature}*F", True, (255, 255, 255))
    screen.blit(text_humidity,(100,100))
    screen.blit(text_temperature,(100,200))
    
  
   
def camThread():

    while (code_run):
        curr_time = time.time()
        try:
            plantCam.generate_preview(screen)
        except:
            pass

def timestampThread():

    while (code_run):
        try:
            date = datetime.datetime.today().strftime('%H:%M:%S %Y-%m-%d')
            timestamp_text= font_sm.render(f"Current Time: {date} " , True, (DARK_GREEN))
            timestamp_rect = timestamp_text.get_rect(center=(90,10))
            screen.fill(LIGHT_GREEN,timestamp_rect)
            pygame.display.update()
            screen.blit(timestamp_text,timestamp_rect)
            time.sleep(1)
        except:
            pass

curr_time = time.time()
init_time = time.time()
while (code_run and curr_time < init_time + 10):
    curr_time = time.time()

    events=pygame.event.get()
    pitft.update() #refresh touchscreen
    for e in events:
        if (e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE):
            print('Quit Callback')
            code_run = False 
            # filename = 'image.jpg'
            # print('Capturing frame...')
            # camera.switch_mode_and_capture_file(configStill, filename)
            
            # print('Displaying the captured frame for 5 seconds...')
            # capturedFrame = pygame.image.load(filename).convert()
            # capturedFrameRectangle = capturedFrame.get_rect()
            # screen.blit(capturedFrame, capturedFrameRectangle)
            # pygame.display.update()
            # time.sleep(5)

    if menu_level_1:
        screen.fill((LIGHT_GREEN))
        screen.blit(text_surface2,(100,100))
        for e in events:
            if(e.type is MOUSEBUTTONUP):
                x,y = pygame.mouse.get_pos()
                text_surface3 = font_big.render(f' Touch at ({x},{y}) ', True, (DARK_GREEN))
                rect1 = text_surface3.get_rect(center=(160,100))
                screen.blit(text_surface3, rect1)                     
                if ( y > 200 ):       
                    print('entering menu 2')
                    menu_level_1 = False
                    menu_level_2 = True
                    start_preview = True
                    screen.fill((LIGHT_GREEN))
                    pygame.display.update()
                    
    elif menu_level_2: 

        if (start_preview):
            #blit once when preview starts--
            screen.blit(text_surface,(40,80))
            screen.blit(sun_icon,(200,50))
            screen.blit(temp_icon,(200,100))
            screen.blit(water_icon,(200,160))
            start_preview = False
            t1 = Thread(target=camThread)
            t1.start()
            t2 = Thread(target=timestampThread)
            t2.start()
    pygame.display.update()
code_run = False # update code_run to false on timeout
    
screen.fill((LIGHT_GREEN))
pygame.display.update()
plantCam.close()
if t1.is_alive():
    t1.join()
if t2.is_alive():
    t2.join()
pygame.quit()
GPIO.cleanup()
del(pitft) # stop touch monitoring
sys.exit()

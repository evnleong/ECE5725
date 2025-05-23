import pygame,pigame
from pygame.locals import *
import time,datetime
import os
import sys
import RPi.GPIO as GPIO
from threading import Thread, Event
from camera import PlantCamera
from light import GrowLight
from thsensor import THSensor
from pump import PlantPump
from msensor import MSensor,detect_moisture
import web
from globals import plant_data

stop_event = Event()

# Environment Setup 
os.putenv('SDL_VIDEODRV','fbcon')
os.putenv('SDL_FBDEV', '/dev/fb1')
os.putenv('SDL_MOUSEDRV','dummy')
os.putenv('SDL_MOUSEDEV','/dev/null')
os.putenv('DISPLAY','')

# Setup GPIO for TFT 
GPIO.setmode(GPIO.BCM)   
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(6,GPIO.OUT,initial = GPIO.HIGH)

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


#Fonts + Text
font_big = pygame.font.Font(None, 35)
font_med = pygame.font.Font(None, 20)
font_sm = pygame.font.Font(None,15)
video_title_text = font_sm.render("Live Camera", True, (DARK_GREEN))
welcome_text= font_big.render("Welcome!", True, (DARK_GREEN))
enter_text = font_med.render("Press Button #17 to Enter", True, (DARK_GREEN))
text_surface3 = font_big.render("Temp:", True, (DARK_GREEN))
timestamp_text = font_sm.render(f"Date: {date} " , True, (DARK_GREEN))
brightup_text = font_sm.render(f"< Brightness Up" , True, (DARK_GREEN))
brightdown_text = font_sm.render(f"< Brightness Down" , True, (DARK_GREEN))
pump_text = font_sm.render(f"< Increase Humidity" , True, (DARK_GREEN))
quit_text = font_sm.render(f"<  Quit" , True, (DARK_GREEN))
stats_text = font_med.render(f"Greenhouse Statistics" , True, (DARK_GREEN))
 

screen = pygame.display.set_mode((appWidth, appHeight))
plantCamSuccess = True
# camera = Picamera2()

code_run = True

try:
    plantCam = PlantCamera()

except:
    code_run= False
    plantCamSuccess =False

growLight = GrowLight(pin=16)
thSensor = THSensor(pin=20)

try:
    waterPump = PlantPump(pin = 6)
except Exception as e:
    raise e
mSensor = MSensor(pin=26)

# Assets 
sun_icon = pygame.transform.scale(pygame.image.load(os.path.join('assets','sun.png')), (40,40))
temp_icon = pygame.transform.scale(pygame.image.load(os.path.join('assets','temp.png')), (50,50))
water_icon= pygame.transform.scale(pygame.image.load(os.path.join('assets','water.png')), (50,50))

menu_level_1 =  True
menu_level_2 = False
start_preview = False

# Callbacks

def button27(channel):
      growLight.increaseDutyCycle()

def button23(channel):
      growLight.decreaseDutyCycle()

def button22(channel):
      print("pump on")
      waterPump.pump_on()
    

def button17(channel):
    print('Entering Main Menu')
    global menu_level_1, menu_level_2, start_preview
    menu_level_1 = False
    menu_level_2 = True
    start_preview = True
    screen.fill((LIGHT_GREEN))
    pygame.display.update()

# Add event listeners
GPIO.add_event_detect(27, GPIO.RISING, callback = button27, bouncetime =200)
GPIO.add_event_detect(23, GPIO.RISING, callback = button23, bouncetime =200)
GPIO.add_event_detect(22, GPIO.RISING, callback = button22, bouncetime =700)
GPIO.add_event_detect(17, GPIO.RISING, callback = button17, bouncetime =200)



def temphumidityThread():
    while code_run:
        try:
            text_light_level = font_med.render(f"Light Level: {growLight.dutyCycle}%",True,(DARK_GREEN) )
            light_level_rect = text_light_level.get_rect(center=(230,50))


            humidity,temperature = thSensor.update_ht()
            text_humidity = font_med.render(f"Humidity: {humidity}%", True, (DARK_GREEN))
            text_temperature = font_med.render(f"Temp: {temperature}*F", True, (DARK_GREEN))
            humidity_rect = text_humidity.get_rect(center=(230,150))
            temperature_rect = text_temperature.get_rect(center=(225,100))
            moisture = plant_data['moisture']
            text_moisture = font_med.render(f"Moisture: {moisture}", True, (DARK_GREEN))
            moisture_rect = text_moisture.get_rect(center=(230,180))
       
            screen.fill(LIGHT_GREEN,humidity_rect)
            screen.fill(LIGHT_GREEN,temperature_rect)
            screen.fill(LIGHT_GREEN,light_level_rect)
            screen.fill(LIGHT_GREEN,moisture_rect)
            pygame.display.update()
            screen.blit(text_humidity,humidity_rect)
            screen.blit(text_temperature,temperature_rect)
            screen.blit(text_light_level,light_level_rect)
            screen.blit(text_moisture,moisture_rect)
            time.sleep(1)

            plant_data['temperature'] = temperature
            plant_data['humidity'] = humidity
            plant_data['light_level'] = growLight.dutyCycle
            # plant_data['moisture'] = moisture 
            plant_data['pump_status'] = waterPump.state
        except Exception as e:
            print(e)
    

   
# def camThread():

#     while code_run:
#         curr_time = time.time()
#         try:
#             plantCam.generate_preview(screen)
#         except:
#             pass

def timestampThread():

    while code_run:
        try:
            date = datetime.datetime.today().strftime('%H:%M:%S %Y-%m-%d')
            timestamp_text= font_sm.render(f"Current Time: {date} " , True, (DARK_GREEN))
            timestamp_rect = timestamp_text.get_rect(center=(90,230))
            screen.fill(LIGHT_GREEN,timestamp_rect)
            pygame.display.update()
            screen.blit(timestamp_text,timestamp_rect)
            time.sleep(1)
        except:
            pass

curr_time = time.time()
init_time = time.time()
flask_thread_started = False


while (code_run and curr_time < init_time + 360):
    curr_time = time.time()

    events=pygame.event.get()
    pitft.update() #refresh touchscreen
    for e in events:
        if (e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE):
            print('Quit Callback')
            code_run = False 
          

    if menu_level_1:
        screen.fill((LIGHT_GREEN))
        screen.blit(welcome_text,(100,100))
        screen.blit(enter_text,(80,160))
        # for e in events:
        #     if(e.type is MOUSEBUTTONUP):
        #         x,y = pygame.mouse.get_pos()
        #         text_surface3 = font_big.render(f' Touch at ({x},{y}) ', True, (DARK_GREEN))
        #         rect1 = text_surface3.get_rect(center=(160,100))
        #         screen.blit(text_surface3, rect1)                     
        #         if ( y > 200 ):       
        #             print('entering menu 2')
        #             menu_level_1 = False
        #             menu_level_2 = True
        #             start_preview = True
        #             screen.fill((LIGHT_GREEN))
        #             pygame.display.update()
                    
    elif menu_level_2: 

        if (start_preview):
            #blit once when preview starts--
            screen.fill((LIGHT_GREEN))
            screen.blit(sun_icon,(130,25))
            screen.blit(temp_icon,(130,75))
            screen.blit(water_icon,(130,145))
            screen.blit(brightup_text,(10,0))
            screen.blit(brightdown_text,(10,60))
            screen.blit(pump_text,(10,120))
            screen.blit(quit_text,(10,190))
            screen.blit(stats_text,(145,10))
            if not flask_thread_started:
                web.start_flask_thread(plantCam,growLight)
                flask_thread_started = True
            elif flask_thread_started: #if button 17 pressed again, quit
                code_run = False
            start_preview = False
            t1 = Thread(target=temphumidityThread)
            t1.start()
            t2 = Thread(target=timestampThread)
            t2.start()
    pygame.display.update()
code_run = False # update code_run to false on timeout
screen.fill((LIGHT_GREEN))
growLight.light_off()
pygame.display.update()
if plantCamSuccess:
    plantCam.close()
# if t1.is_alive():
#     t1.join()
# if t2.is_alive():
#     t2.join()
pygame.quit()
GPIO.cleanup()
del(pitft) # stop touch monitoring
sys.exit()

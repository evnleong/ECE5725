#Class Definition for Raspberry Pi Camera 2 
from picamera2 import Picamera2
from libcamera import ColorSpace
import pygame
import cv2


appWidth = 640
appHeight = 480

class PlantCamera():

    def __init__(self):
        try:
            self.previewWidth = int(appWidth)
            self.previewHeight = int(appHeight)
            self.camera = Picamera2()
            
            #Camera initialization + config
            configPreview = self.camera.create_preview_configuration()
            self.camera.preview_configuration.main.size = (self.previewWidth, self.previewHeight)
            self.camera.preview_configuration.main.format = 'BGR888'
            self.camera.configure('preview')
            configStill = self.camera.create_still_configuration()
            self.camera.still_configuration.enable_raw()
            self.camera.still_configuration.main.size = self.camera.sensor_resolution
            self.camera.still_configuration.buffer_count = 2
            self.camera.still_configuration.colour_space = ColorSpace.Sycc()
            self.camera.start()
        except:
            raise Exception 


    #takes tft screen object and blits camera preview to it
    def generate_preview(self, screen):
        array = self.camera.capture_array()
        previewFrame = pygame.image.frombuffer(array.data, (self.previewWidth, self.previewHeight), 'RGB')
        screen.blit(previewFrame, (0, 100))

    def close(self):
        self.camera.close()

    def save_frame(self,screen):
        pass
        # filename = 'image.jpg'
        # print('Capturing frame...')
        # camera.switch_mode_and_capture_file(configStill, filename)
        # print('Displaying the captured frame for 5 seconds...')
        # capturedFrame = pygame.image.load(filename).convert()
        # capturedFrameRectangle = capturedFrame.get_rect()
        # screen.blit(capturedFrame, capturedFrameRectangle)
        # pygame.display.update()
        # time.sleep(5)

    def get_frame(self):
        try:
            frame = self.camera.capture_array()
            # ret, jpeg = cv2.imencode('.jpg', frame)
            # return jpeg.tobytes()
            frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            ret, jpeg = cv2.imencode('.jpg', frame_bgr)
            return jpeg.tobytes()
        except Exception as e:
            print("Camera capture error:", e)
            return None




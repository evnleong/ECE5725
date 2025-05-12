#Class Definition for Raspberry Pi Camera 2 
from picamera2 import Picamera2
from libcamera import ColorSpace
import pygame


appWidth = 320
appHeight = 240

class PlantCamera():

    def __init__(self):
        try:
            self.previewWidth = int(appWidth/2)
            self.previewHeight = int(appHeight/2)
            self.camera = Picamera2()

            # === Create Configurations ====================================================

            configPreview = self.camera.create_preview_configuration()
            self.camera.preview_configuration.main.size = (self.previewWidth, self.previewHeight)
            self.camera.preview_configuration.main.format = 'BGR888'
            self.camera.configure('preview')

            # ------------------------------------------------------------------------------

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





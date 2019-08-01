from picamera import PiCamera, Color
from picamera.array import PiRGBArray
from time import sleep

# --------------------------------------------------------------------------------------------------------------
# ------------------------------- Raspberry Pi Camera Setup Class ----------------------------------------------
# -------------------------------------------------------------------------------------------------------------- 
class Setup_PiCam(object):
        def __init__(self):
                self.camera = None
                  
        # Instantiate PiCamera module
        def PiCam_Configuration(self):
                self.camera = PiCamera()  
                self.camera.rotation = 180
                self.rawCapture = PiRGBArray(self.camera)

                # allow the camera to warmup
                sleep(0.1)
                
                #~ return self.camera
                return self.camera, self.rawCapture
                


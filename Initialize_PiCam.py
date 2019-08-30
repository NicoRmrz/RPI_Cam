from picamera import PiCamera, Color
from picamera.array import PiRGBArray
from time import sleep
from CameraLED import CameraLED

# --------------------------------------------------------------------------------------------------------------
# ------------------------------- Raspberry Pi Camera Setup Class ----------------------------------------------
# -------------------------------------------------------------------------------------------------------------- 
class Setup_PiCam(object):
        def __init__(self):
                self.camera = None
                  
        # Instantiate PiCamera module
        def PiCam_Configuration(self):
                self.camera = PiCamera()  
                self.led = CameraLED() # CameraLED(134)
                self.camera.rotation = 180
                self.rawCapture = PiRGBArray(self.camera)

                # allow the camera to warmup
                sleep(0.1)

                #~ # between on and off
                for i in range(2):
                        for x in range(3):
                                self.led.on()
                                sleep(0.15)
                                self.led.off()
                                sleep(0.15)
         
                        self.led.on()
                        #print(self.led.state())     
                        sleep(0.5)
                                        
                        self.led.toggle()
                
                #~ return self.camera
                return self.camera, self.rawCapture, self.led
                


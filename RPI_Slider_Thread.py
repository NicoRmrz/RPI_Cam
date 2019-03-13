from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot
from time import sleep


class QSliderThread(QThread):

    brightnessLabel_Sig = pyqtSignal(int)
    contrastLabel_Sig = pyqtSignal(int)
    sharpnessLabel_Sig = pyqtSignal(int)
    saturationLabel_Sig = pyqtSignal(int)
    annotationLabel_Sig = pyqtSignal(int)
    framerate_Sig = pyqtSignal(int)
    
    
    def __init__(self, RPICamera):
        QThread.__init__(self)
        self.camera = RPICamera
        self.exitProgram = False
        self.brightnessSlider = False
        self.contrastSlider = False
        self.sharpnessSlider = False
        self.saturationSlider = False
        self.annotationSlider = False
  
    # Set to update value of brightness slider
    def set_brightnessSlider(self, string, newNum):
        self.brightnessSlider = string
        self.brightnessValue = newNum
  
    # Set to update value of contrast slider
    def set_contrastSlider(self, string, newNum):
        self.contrastSlider = string
        self.contrastValue = newNum
  
    # Set to update value of sharpness slider
    def set_sharpnessSlider(self, string, newNum):
        self.sharpnessSlider = string
        self.sharpnessValue = newNum
  
    # Set to update value of saturation slider
    def set_saturationSlider(self, string, newNum):
        self.saturationSlider = string
        self.saturationValue = newNum
  
    # Set to update value of annotation text
    def set_annotationSlider(self, string, newNum):
        self.annotationSlider = string
        self.annotationValue = newNum

    #Sets up the program to exit when the main window is shutting down
    def Set_Exit_Program(self, exiter):
        self.exitProgram = exiter

    #This function is started by .start() and runs the main portion of the code
    def run(self):

        while(1):
            
            #set for brightness slider to increment
            if self.brightnessSlider != False:        
                self.UpdateBrightnessLabel(self.brightnessValue)
                self.camera.brightness = self.brightnessValue 
                self.brightnessSlider = False
            
            #set for contrast slider to increment
            if self.contrastSlider != False:        
                self.UpdateContrastLabel(self.contrastValue)
                self.camera.contrast = self.contrastValue 
                self.contrastSlider = False
            
            #set for sharpness slider to increment
            if self.sharpnessSlider != False:        
                self.UpdateSharpnessLabel(self.sharpnessValue)
                self.camera.sharpness = self.sharpnessValue 
                self.sharpnessSlider = False
            
            #set for saturation slider to increment
            if self.saturationSlider != False:        
                self.UpdateSaturationLabel(self.saturationValue)
                self.camera.saturation = self.saturationValue 
                self.saturationSlider = False
            
            #set for annotation slider to increment
            if self.annotationSlider != False:        
                self.UpdateAnnotationLabel(self.annotationValue)
                self.camera.annotate_text_size = self.annotationValue 
                self.annotationSlider = False
                
            if(self.exitProgram == True):
                self.exitProgram = False
                break

            sleep(0.5)

    def UpdateBrightnessLabel(self, value):
        self.brightnessLabel_Sig.emit(value)
            
    def UpdateContrastLabel(self, value):
        self.contrastLabel_Sig.emit(value)
            
    def UpdateSharpnessLabel(self, value):
        self.sharpnessLabel_Sig.emit(value)
            
    def UpdateSaturationLabel(self, value):
        self.saturationLabel_Sig.emit(value)
            
    def UpdateAnnotationLabel(self, value):
        self.annotationLabel_Sig.emit(value)
        
   
  

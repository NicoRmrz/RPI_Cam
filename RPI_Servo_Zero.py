import board 
import busio
#from adafruit_pca9685 import PCA9685 # Import the PCA9685 module.
from PCA9685 import PCA9685 # Import the PCA9685 module.
from adafruit_motor import servo
from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot
from time import sleep

# --------------------------------------------------------------------------------------------------------------
# ------------------------------ I2C Servo Initialization Class ------------------------------------------------
# -------------------------------------------------------------------------------------------------------------- 
class Initialize_Servo(object):
        def __init__(self):
            # Create a simple PCA9685 class instance.
            self.pwm = PCA9685(0x40)
            # Set the PWM frequency to 50hz
            self.pwm.setPWMFreq(50)

            self.pwm.setServoPulse(0,1500)
            self.pwm.setServoPulse(1,1500)

# --------------------------------------------------------------------------------------------------------------
# ------------------------------ Horizontal Servo Movement Thread Class ----------------------------------------
# -------------------------------------------------------------------------------------------------------------- 
class QServoHorizontalThread(QThread):

    horizontal_Sig = pyqtSignal(str, str)
    Btn_Handler = pyqtSignal(str)
    
    def __init__(self, PiServo, horizontal_pos):
        QThread.__init__(self)
        self.PiServo = PiServo
        self.exitProgram = False
        self.left = False
        self.right = False
        self.setYPOS = False
        self.horizontalPosition = horizontal_pos
        
       # self.upDownMotor = self.PiServo.upDownMotor
        #self.leftRightMotor = self.PiServo.leftRightMotor
       # self.hat = self.PiServo.hat
        
    # Set to move camera left
    def set_leftButton(self, string):
        self.left = string
        if (self.horizontalPosition <= 2500): # Set max limit
            self.horizontalPosition = self.horizontalPosition + 10
        else:
            self.horizontalPosition = self.horizontalPosition
        
    # Set to move camera right
    def set_rightButton(self, string):
        self.right = string
        if (self.horizontalPosition >= 500): # Set min limit
            self.horizontalPosition = self.horizontalPosition - 10
        else:
            self.horizontalPosition = self.horizontalPosition
               
    # Set track pad Y position
    def set_Y_POS(self, setY, Y):
        self.setYPOS = setY
        self.yPosition = Y
    
    # Sets up the program to exit when the main window is shutting down
    def Set_Exit_Program(self, exiter):
        self.exitProgram = exiter

    # This function is started by .start() and runs the main portion of the code
    def run(self):

        while(1):
            
            # Set Y value of track pad to servo position
            #if self.setYPOS != False:
            #    try:
            #        self.leftRightMotor.angle = self.yPosition
            #    except ValueError as e: 
            #        print(e)
            #    finally:
            #        self.setYPOS = False
            
            #Set for left key "A" to move camera left
            if self.left != False:
                if (self.horizontalPosition >=500 and self.horizontalPosition <= 2500):
                   # self.leftRightMotor.angle = self.horizontalPosition
                    self.PiServo.pwm.setServoPulse(1,self.horizontalPosition)
                    self.horizontalDone("horizontalMotor", str(self.horizontalPosition))         #Emit new position of servo
                    
                elif (self.horizontalPosition < 50):
                    self.horizontalDone("horizontalMotor", "Min")
                    
                elif (self.horizontalPosition > 2500):
                    self.horizontalDone("horizontalMotor", "Max")
                    
                self.ButtonHandler("Left")
                self.left = False
                     
            #Set for right key "D" to move camera right
            if self.right != False:
                if (self.horizontalPosition >=500 and self.horizontalPosition <= 2500):
                    self.PiServo.pwm.setServoPulse(1,self.horizontalPosition)
                    self.horizontalDone("horizontalMotor", str(self.horizontalPosition))         #Emit new position of servo
                    
                elif (self.horizontalPosition < 50):
                    self.horizontalDone("horizontalMotor", "Min")
                    
                elif (self.horizontalPosition > 2500):
                    self.horizontalDone("horizontalMotor", "Max")
                    
                self.ButtonHandler("Right")
                self.right = False
        
                
            if(self.exitProgram == True):
               # self.hat.deinit() # To stop using pca9685
                self.exitProgram = False
                break

            sleep(0.01)

    def horizontalDone(self, string, value):
        self.horizontal_Sig.emit(string, value)
        
    def ButtonHandler(self, string):
        self.Btn_Handler.emit(string)
# --------------------------------------------------------------------------------------------------------------
# ------------------------------ Vertical Servo Movement Thread Class ----------------------------------------
# -------------------------------------------------------------------------------------------------------------- 
class QServoVerticalThread(QThread):

    vertical_Sig = pyqtSignal(str, str)
    Btn_Handler = pyqtSignal(str)
    
    def __init__(self, PiServo, vertical_pos):
        QThread.__init__(self)
        self.PiServo = PiServo
        self.exitProgram = False
        self.up = False
        self.down = False
        self.setXPOS = False
        self.verticalPosition = vertical_pos
        
        #~ self.upDownMotor = self.PiServo.upDownMotor
        #~ self.leftRightMotor = self.PiServo.leftRightMotor
        #~ self.hat = self.PiServo.hat

    # Set to move camera up
    def set_upButton(self, string):
        self.up = string
        if (self.verticalPosition <= 500): # Set min limit
            self.verticalPosition = self.verticalPosition 
        else:
            self.verticalPosition = self.verticalPosition - 10
        
    # Set to move camera down
    def set_downButton(self, string):
        self.down = string
        if (self.verticalPosition <= 2500): # Set max limit
            self.verticalPosition = self.verticalPosition + 10
        else:
            self.verticalPosition = self.verticalPosition
            
    # Set track pad Y position
    def set_X_POS(self, setX, X):
        self.setXPOS = setX
        self.xPosition = X

    # Sets up the program to exit when the main window is shutting down
    def Set_Exit_Program(self, exiter):
        self.exitProgram = exiter

    # This function is started by .start() and runs the main portion of the code
    def run(self):

        while(1):
            
            # Set Y value of track pad to servo position
            #if self.setXPOS != False:
            #    try:
            #        self.upDownMotor.angle = self.xPosition
            #    except ValueError as e: 
            #        print(e)
            #    finally:
            #        self.setXPOS = False
            
            #Set for left key "W" to move camera up
            if self.up != False:
                if (self.verticalPosition >50 and self.verticalPosition <= 2500):
                    self.PiServo.pwm.setServoPulse(0,self.verticalPosition)
                    self.verticalDone("verticalMotor", str(self.verticalPosition))         #Emit new position of servo
                    
                elif (self.verticalPosition <= 50):
                    self.verticalDone("verticalMotor", "Min")
                    
                elif (self.verticalPosition > 2500):
                    self.verticalDone("verticalMotor", "Max")
                    
                self.ButtonHandler("Up")
                self.up = False
       
            #Set for left key "S" to move camera down
            if self.down != False:
                if (self.verticalPosition >50 and self.verticalPosition <= 2500):
                    self.PiServo.pwm.setServoPulse(0,self.verticalPosition)
                    self.verticalDone("verticalMotor", str(self.verticalPosition))         #Emit new position of servo
                    
                elif (self.verticalPosition <= 50):
                    self.verticalDone("verticalMotor", "Min")
                    
                elif (self.verticalPosition > 2500):
                    self.verticalDone("verticalMotor", "Max")
                    
                self.ButtonHandler("Down")
                self.down = False
      
            if(self.exitProgram == True):
               # self.hat.deinit() # To stop using pca9685
                self.exitProgram = False
                break

            sleep(0.01)
        
    def verticalDone(self, string, value):
        self.vertical_Sig.emit(string, value)
        
    def ButtonHandler(self, string):
        self.Btn_Handler.emit(string)
# --------------------------------------------------------------------------------------------------------------
# ------------------------------ Free Movement Track Pad Thread Class ------------------------------------------
# -------------------------------------------------------------------------------------------------------------- 
class QServoTrackPadThread(QThread):

    upDown_Sig = pyqtSignal(int)
    leftRight_Sig = pyqtSignal(int)
    horizontal_Sig = pyqtSignal(str, str)
    vertical_Sig = pyqtSignal(str, str)
    Btn_Handler = pyqtSignal(str)
    
    def __init__(self, PiServo, horizontal_pos, vertical_pos):
        QThread.__init__(self)
        self.PiServo = PiServo
        self.exitProgram = False
        self.upDownSlider = False
        self.leftRightSlider = False
        self.horizontalPosition = horizontal_pos
        self.verticalPosition = vertical_pos
        
   
        
    # Set to update value of Up Down Servo slider
    def set_upDownSlider(self, string, newNum):
        self.upDownSlider = string
        self.upDownValue = 180 - newNum
  
    # Set to update value of Left Right Servo slider
    def set_leftRightSlider(self, string, newNum):
        self.leftRightSlider = string
        self.leftRightValue = 180 - newNum
        
    # Sets up the program to exit when the main window is shutting down
    def Set_Exit_Program(self, exiter):
        self.exitProgram = exiter

    # This function is started by .start() and runs the main portion of the code
    def run(self):

        while(1):
           
            # set for upDownSlider servo to move
            if self.upDownSlider != False:        
                #self.upDownMotor.angle = self.upDownValue
                self.upDownDONE(self.upDownValue)
                self.upDownSlider = False
            
            # set for leftRight servo to move
            if self.leftRightSlider != False:        
               # self.leftRightMotor.angle = self.leftRightValue 
                self.leftRightDONE(self.leftRightValue)
                self.leftRightSlider = False
                
            if(self.exitProgram == True):
               # self.hat.deinit() # To stop using pca9685
                self.exitProgram = False
                break

            sleep(0.1)

    def horizontalDone(self, string, value):
        self.horizontal_Sig.emit(string, value)
        
    def verticalDone(self, string, value):
        self.vertical_Sig.emit(string, value)
        
    def ButtonHandler(self, string):
        self.Btn_Handler.emit(string)
            

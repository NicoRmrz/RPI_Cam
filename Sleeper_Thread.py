from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot
from time import sleep


class QTimeThread(QThread):

    time_signal = pyqtSignal(int)
    sleep_signal = pyqtSignal(int)
    delay_signal = pyqtSignal(int)
    dropdown_signal = pyqtSignal(int)
        
    def __init__(self):
        QThread.__init__(self)
        self.exitProgram = False
        self.time_to_wait = 0
        self.time_state = False 
        self.time_sleep = 0
        self.setSleep = False 
        self.time_to_sleep = 0
        self.setSleepState = False 
        self.waitTime = 0
        self.sleepState = False 
        
    # Timer for capture button, display time for image on GUI
    def set_Timer(self, input, State):
        self.time_to_wait = input
        self.time_state = State
        
    # Timer for record button, wait for stream to pause    
    def set_recTimer(self, input, State):
        self.time_sleep = input
        self.setSleep = State
    
    # Timer for time lapse button, wait for stream to pause     
    def set_timeLapseTimer(self, input, State):
        self.time_to_sleep = input
        self.setSleepState = State
    
    # Timer for time lapse button, wait for stream to pause     
    def set_dropDownTimer(self, input, State):
        self.waitTime = input
        self.sleepState = State

    #Sets up the program to exit when the main window is shutting down
    def Set_Exit_Program(self, exiter):
        self.exitProgram = exiter

    #This function is started by .start() and runs the main portion of the code
    def run(self):

        while(1):
            
            #Timer for capture button, display time for image on GUI
            if self.time_state != False:        
                sleep(self.time_to_wait)
                self.Time_finished(self.time_to_wait)
                self.time_state = False
                
            # Timer for record button, wait for stream to pause     
            if self.setSleep != False:         
                sleep(self.time_sleep)
                self.Time_Sleep_Done(self.time_sleep)
                self.setSleep = False
            
            # Timer for time lapse button, wait for stream to pause     
            if self.setSleepState != False:
                sleep(self.time_to_sleep)
                self.Timer_Done_TLapse(self.time_to_sleep)
                self.setSleepState = False
            
            # Timer for drop down button, wait for stream to pause     
            if self.sleepState != False:
                sleep(self.time_to_sleep)
                self.Timer_Done_DrpDwn(self.waitTime)
                self.sleepState = False

            if(self.exitProgram == True):
                self.exitProgram = False
                break

            sleep(1)

            
    def Time_finished(self, time_in):
        self.time_signal.emit(time_in)
        
    def Time_Sleep_Done(self, time_in):
        self.sleep_signal.emit(time_in)
        
    def Timer_Done_TLapse(self, time_in):
        self.delay_signal.emit(time_in)
        
    def Timer_Done_DrpDwn(self, time_in):
        self.dropdown_signal.emit(time_in)

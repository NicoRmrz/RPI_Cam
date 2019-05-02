import datetime
import os
import time
import sys
import PyQt5
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLineEdit, QLabel, QCheckBox, QTextEdit, QProgressBar, QSizePolicy, QWidget, QTabWidget, QHBoxLayout, QVBoxLayout, QSlider
from PyQt5.QtGui import QPixmap, QIcon, QFont, QTextCursor, QPalette, QImage, QBrush
from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot, QObject, QSize
from GUI_Stylesheets import GUI_Stylesheets

# Instantiate style sheets for GUI Objects
GUI_Style = GUI_Stylesheets()

RECORD_TIME = 100        # 100 seconds

# Icon Image locations
Main_path = os.getcwd() + "/"     
Icon_Path = Main_path + 'Icon_Image/pup.jpg'
Camera_Idle_Path = Main_path + 'Icon_Image/cam_idle.png'
Camera_Capture_Path = Main_path + 'Icon_Image/cam_capture.png'
Video_Idle_Path = Main_path + 'Icon_Image/video_idle.png'
Video_Recording_Path = Main_path + 'Icon_Image/video_recording.png'
Stop_Idle_Path = Main_path + 'Icon_Image/stop_idle.png'
Stop_Greyed_Path = Main_path + 'Icon_Image/stop_grey.png'
TimeLapse_Idle_Path = Main_path + 'Icon_Image/timelapse_idle1.png'
TimeLapse_InUse_Path = Main_path + 'Icon_Image/timelapse_inuse.png'
Main_Tab_Path = Main_path + 'Icon_Image/mainTab.png'
Settings_Tab_Path = Main_path + 'Icon_Image/settingsTab.png'

#GUI Classes
#This is the class for push buttons from the Pyqt 5 framework
class Snapshot_Button(QPushButton):         #Capture image button
    old_window = None
    new_window = None

    # Initializes the necessary objects into the button class for control
    def __init__(self, window, text, input_largetextbox, capture_thread, Vid_Stream, TimeThread, record_thread, TimeLapse_Thread):
        super(Snapshot_Button, self).__init__()
        self.setText(text)
        self.setParent(window)
        self.large_textbox = input_largetextbox
        self.captureThread = capture_thread
        self.Video_Stream = Vid_Stream
        self.TimerThread = TimeThread
        self.recordThread = record_thread
        self.timelapseThread = TimeLapse_Thread
        
        #Connecting completions signals to functions
        self.captureThread.Snap_Captured_signal.connect(self.Snapshot_Captured)    
        self.TimerThread.time_signal.connect(self.Timer_Finished)   
        self.captureThread.Status_Signal.connect(self.Camera_Status)    
        self.captureThread.Capture_Terminated_signal.connect(self.Camera_Stopped)

    # Function call for the click event
    def On_Click(self):
        self.WriteToConsole("Capturing Image")
        
        # Button turns red for activated
        self.setIcon(QIcon(Camera_Capture_Path))

    # Function call for the Un_click event
    def Un_Click(self):
        #Stop video stream to capture image
        self.Video_Stream.Set_Video_Stream_Ready(False)
       
        #Take a picture
        self.captureThread.Set_Snapshot_Ready(True)
        self.captureThread.Set_Stop(False)      # set stop button to false
        self.recordThread.Set_Snapshot_Ready(True)  #let other  thread know capture button was pressed
        self.timelapseThread.Set_Snapshot_Ready(True) #let other  thread know capture button was pressed
        
    #Function for picture capture completion
    def Snapshot_Captured(self, Snap_done):
        self.Snap_captured = Snap_done
        self.WriteToConsole(self.Snap_captured)
        
        #Display picture taken for 3 seCamera_Statusconds
        self.TimerThread.set_Timer(1.5, True)
    
    #Function for completion of timer    
    def Timer_Finished(self, timeout):
        self.Timeout = timeout
        
        #set to find out if camera is ready
        self.captureThread.Get_Rec_Status()
        
    #Function to reset GUI object pending on recording status
    def Camera_Status(self, rec_status):
        self.status = rec_status

        if (self.status > 0):
            self.setIcon(QIcon(Camera_Idle_Path)) 
            self.Reset_GUI() 
        else:
            self.Reset_GUI() 
        
    #Function when stopped button is pressed
    def Camera_Stopped(self, text):
        self.stopText = text 
        self.Reset_GUI() 
        
    #Resets the necessary objects when the test is reran
    def Reset_GUI(self):
        self.Video_Stream.Set_Video_Stream_Ready(True) #Continue video stream 
        self.setIcon(QIcon(Camera_Idle_Path))

    # Function call to write to Console Log
    def WriteToConsole(self, new_input):
        self.old_window = self.large_textbox.toPlainText()
        self.new_window = self.old_window + '\n' + new_input
        self.large_textbox.setText(self.new_window)
        self.large_textbox.moveCursor(QTextCursor.End)

class Record_Button(QPushButton):       #Record Button
    old_window = None
    new_window = None

    # Initializes the necessary objects into the button class for control
    def __init__(self, window, text, input_largetextbox, record_thread, ProgressBar, Vid_Stream, PbarUpdater, capture_thread, TimeLapse_Thread, TimeThread):
        super(Record_Button, self).__init__()
        self.setText(text)
        self.setParent(window)
        self.large_textbox = input_largetextbox
        self.recordThread = record_thread
        self.captureThread = capture_thread
        self.Progress_Bar = ProgressBar
        self.Video_Stream = Vid_Stream
        self.PBarThread = PbarUpdater
        self.timelapseThread = TimeLapse_Thread
        self.TimerThread = TimeThread
        
        #Connecting thread (emits) to functions
        self.PBarThread.Update_prog_bar_signal.connect(self.Update_Progress_Bar) 
        self.recordThread.Recording_Completed_signal.connect(self.Video_Finished)
        self.recordThread.Recording_Terminated_signal.connect(self.Video_Stopped)
        self.TimerThread.sleep_signal.connect(self.PostPauseStream)
        self.recordThread.Snap_while_recording_signal.connect(self.CaptureWhileRecording)

    # Function call for the click event
    def On_Click(self):        
        #Rests progress bar
        self.Progress_Bar.reset()

    # Function call for the Un_click event
    def Un_Click(self):
        
        #Stop video stream to record a video
        self.Video_Stream.Set_Video_Stream_Ready(False)
        
        #Wait for stream to pause
        self.TimerThread.set_recTimer(0.5, True)
                  
    def PostPauseStream(self, timeout):
        self.Timeout = timeout
        
         # Button turns red for activated
        self.setIcon(QIcon(Video_Recording_Path))
        
        #Set thread to record video
        self.recordThread.Set_Record_Ready(True, RECORD_TIME)
        self.recordThread.Set_Stop(False)                 # set stop button to false
        self.recordThread.Set_Snapshot_Ready(False)
        self.captureThread.Set_Record_Ready(True)          #let other  thread know record button was pressed
        self.timelapseThread.Set_Record_Ready(True)        #let other  thread know record button was pressed
        
        #Set progress bar to begin
        self.PBarThread.set_increment_ProgressBar(RECORD_TIME, True)
        self.WriteToConsole("Recording Video for " + str(RECORD_TIME) + " seconds")
        
    # Function to update progress bar    
    def Update_Progress_Bar(self, IncProgBar):
         self.Progress_Bar.setValue(IncProgBar)   
        
    # Function of video completion
    def Video_Finished(self, Video_name):
        self.WriteToConsole(Video_name)
        self.Reset_GUI()
        
    # Function of stop button pressed
    def Video_Stopped(self, str_):
        self.WriteToConsole(str_)
        self.Reset_GUI()
        
    # Function to send name of captured image while recording to console log
    def CaptureWhileRecording(self, imgName):
        self.WriteToConsole(imgName)
                
    # Resets the necessary objects when the procedure is finished
    def Reset_GUI(self):
        self.Video_Stream.Set_Video_Stream_Ready(True) #Continue video stream 
        self.setIcon(QIcon(Video_Idle_Path))

    # Function call to write to Console Log
    def WriteToConsole(self, new_input):
        self.old_window = self.large_textbox.toPlainText()
        self.new_window = self.old_window + '\n' + new_input
        self.large_textbox.setText(self.new_window)
        self.large_textbox.moveCursor(QTextCursor.End)
        
class TimeLapse_Button(QPushButton):    #TimeLapse Button
    old_window = None
    new_window = None

    #Initializes the necessary objects into the button class for control
    def __init__(self, window, text, input_largetextbox, Vid_Stream, record_thread, capture_thread, TimeLapse_Thread, TimeThread, start_button):
        super(TimeLapse_Button, self).__init__()
        self.setText(text)
        self.setParent(window)
        self.large_textbox = input_largetextbox
        self.Video_Stream = Vid_Stream
        self.recordThread = record_thread
        self.captureThread = capture_thread
        self.timelapseThread = TimeLapse_Thread
        self.TimerThread = TimeThread
        self.startBtn = start_button
        
        #Linking signals to functions
        self.timelapseThread.Time_Lapse_String.connect(self.TimeLapseFinished)
        self.timelapseThread.Time_Lapse_imgName.connect(self.Image_Captured)
        self.TimerThread.delay_signal.connect(self.PostPauseStream)
        self.timelapseThread.CaptureWhileTimeLapse.connect(self.captureDuringTimelapse)

    #Function call for the click event
    def On_Click(self):
        # Button turns grey
        self.WriteToConsole("Time Lapse button pressed")
        
    #Function call for the Un_click event
    def Un_Click(self):
        
        #Stop video stream to record a video
        self.Video_Stream.Set_Video_Stream_Ready(False)
        
        #Wait for stream to pause
        self.TimerThread.set_timeLapseTimer(0.5, True)

    def PostPauseStream(self, timeout):
        self.Timeout = timeout
        self.setIcon(QIcon(TimeLapse_InUse_Path))
        
        #Set thread to start time lapse 
        self.timelapseThread.Set_TimeLapse_Ready(True)  
        self.timelapseThread.Set_Stop(False)        # set stop button to false
        self.timelapseThread.Set_Snapshot_Ready(False)
        self.recordThread.Set_TimeLapse_Ready(True) #let other  threads know timelapse button was pressed
        self.captureThread.Set_TimeLapse_Ready(True) #let other  threads know timelapse button was pressed
        
    #Function if timelapse finished and reset GUI buttons
    def TimeLapseFinished(self, TL_str):
        self.TLape_str = TL_str
        self.WriteToConsole("Time Lapse Video Saved as: " + TL_str)
        self.Reset_GUI()

    #Resets the necessary objects when the test is reran
    def Reset_GUI(self):
        self.Video_Stream.Set_Video_Stream_Ready(True) #Continue video stream 
        
        #Turn button color back to normal
        self.setIcon(QIcon(TimeLapse_Idle_Path))
        
   #Function for displaying name of timelapse img to textedit window
    def Image_Captured(self, Snap_done):
        self.Snap_captured = Snap_done
        self.WriteToConsole(self.Snap_captured)
        
   #Function for displaying name when image captured while in time lapse
    def captureDuringTimelapse(self, Snap_done):
        self.captureDuringLapse = Snap_done
        self.WriteToConsole(self.captureDuringLapse)

    # Function call to write to Console Log
    def WriteToConsole(self, new_input):
        self.old_window = self.large_textbox.toPlainText()
        self.new_window = self.old_window + '\n' + new_input
        self.large_textbox.setText(self.new_window)
        self.large_textbox.moveCursor(QTextCursor.End)      

class Stop_Button(QPushButton):         #Stop Button
	old_window = None
	new_window = None

    #Initializes the necessary objects into the button class for control
	def __init__(self, window, text, input_largetextbox, Record_Thread, Record_Button, Vid_Stream, PBar, Capture_Thread, TimeLapse_Thread):
		super(Stop_Button, self).__init__()
		self.setText(text)
		self.setParent(window)
		self.large_textbox = input_largetextbox
		self.recordVideoThread = Record_Thread
		self.RecordBtn = Record_Button
		self.Video_Stream = Vid_Stream
		self.PBar = PBar
		self.captureThread = Capture_Thread
		self.timelapseThread = TimeLapse_Thread

	#Function call for the click event
	def On_Click(self):
		# Button turns grey
		self.setIcon(QIcon(Stop_Greyed_Path))
		
	#Function call for the Un_click event
	def Un_Click(self):

		#Stop all running procedure
		self.recordVideoThread.Set_Stop(True)
		self.captureThread.Set_Stop(True)
		self.timelapseThread.Set_Stop(True)
		self.PBar.Set_Stop_Bar(True)
		self.Reset_GUI()

	# Function call to write to Console Log
	def WriteToConsole(self, new_input):
		self.old_window = self.large_textbox.toPlainText()
		self.new_window = self.old_window + '\n' + new_input
		self.large_textbox.setText(self.new_window)
		self.large_textbox.moveCursor(QTextCursor.End)

	#Resets the necessary objects when the test is reran
	def Reset_GUI(self):
		#Turn button color back to normal
		self.setIcon(QIcon(Stop_Idle_Path))
		self.RecordBtn.setIcon(QIcon(Video_Idle_Path))

class Logo_Button(QPushButton):         # Secret Logobutton
    old_window = None
    new_window = None
    NIGHT_MODE = False

    # Initializes the necessary objects into the button class for control
    def __init__(self, window, text, input_largetextbox, statusBar, xPOS, yPOS, res, consoleLog):
        super(Logo_Button, self).__init__()
        self.setText(text)
        self.setParent(window)
        self.mainWindow = window
        self.large_textbox = input_largetextbox
        self.statusBar = statusBar
        self.xHorizontal = xPOS
        self.yVertical = yPOS
        self.res = res
        self.LargeTextBox = consoleLog

    # Function call for the click event
    def On_Click(self):
        pass

    # Function call for the Un_click event
    def Un_Click(self):
        if self.NIGHT_MODE != True:
            self.Night_Mode()
            self.NIGHT_MODE = True

        elif self.NIGHT_MODE != False:
            self.Regular_Mode()
            self.NIGHT_MODE = False
            
    # Night Mode
    def Night_Mode(self):
        self.mainWindow.setStyleSheet(GUI_Style.NM_mainWindow)
        self.statusBar.setStyleSheet(GUI_Style.NM_statusBarWhite)
        self.xHorizontal.setStyleSheet(GUI_Style.NM_statusBar_XY)
        self.yVertical.setStyleSheet(GUI_Style.NM_statusBar_XY)
        self.res.setStyleSheet(GUI_Style.NM_statusBar_widgets)
        self.LargeTextBox.setStyleSheet(GUI_Style.NM_consoleLog)
        
    # Regular Mode
    def Regular_Mode(self):
        self.mainWindow.setStyleSheet(GUI_Style.mainWindow)
        self.statusBar.setStyleSheet(GUI_Style.statusBarWhite)
        self.xHorizontal.setStyleSheet(GUI_Style.statusBar_XY)
        self.yVertical.setStyleSheet(GUI_Style.statusBar_XY)
        self.res.setStyleSheet(GUI_Style.statusBar_widgets)
        self.LargeTextBox.setStyleSheet(GUI_Style.consoleLog)
        
     # Function call to write to Console Log
    def WriteToConsole(self, new_input):
        self.old_window = self.large_textbox.toPlainText()
        self.new_window = self.old_window + '\n' + new_input
        self.large_textbox.setText(self.new_window)
        self.large_textbox.moveCursor(QTextCursor.End)

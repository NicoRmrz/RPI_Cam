from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot, QObject
from time import sleep
import os


# Icon Image locations
Main_path = os.getcwd() + "/"     
Icon_Path = Main_path + 'Icon_Image/pup.jpg'
Logo_Path = Main_path + 'Icon_Image/logo_icon_white.png'
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
ServoController_Tab_Path = Main_path + 'Icon_Image/controllerTab.png'
Left_Button_Path = Main_path + 'Icon_Image/leftButton.png'
Right_Button_Path = Main_path + 'Icon_Image/rightButton.png'
Up_Button_Path = Main_path + 'Icon_Image/upButton.png'
Down_Button_Path = Main_path + 'Icon_Image/downButton.png'
Freelook_Path = Main_path + 'Icon_Image/freelook1.png'

# Class to reset button icons
class Button_Reset_Handler(QObject):
        def __init__(self, captureThre, recordThre, timelapseThre, PBarThre, capture, record, timelapse, PBar, vidSteam, servoHThre, servoVThre, statusBar, xPosStausbar, yPosStausbar):
                super(Button_Reset_Handler, self).__init__()
                self.captureThread = captureThre
                self.recordThread = recordThre
                self.timelapseThread = timelapseThre
                self.PBarThread = PBarThre
                self.captureBtn = capture
                self.recordBtn = record
                self.timelapseBtn = timelapse
                self.PBar = PBar
                self.Video_Stream = vidSteam
                self.servoHorizontalThread = servoHThre
                self.servoVerticalThread = servoVThre
                self.xPos = xPosStausbar
                self.yPos = yPosStausbar
                self.statusBar = statusBar
                
                # Connect signals to handler function
                self.recordThread.Btn_Handler.connect(self.Button_Handler)
                self.timelapseThread.Btn_Handler.connect(self.Button_Handler)
                self.captureThread.Btn_Handler.connect(self.Button_Handler)
                self.PBarThread.Btn_Handler.connect(self.Button_Handler)
                self.servoHorizontalThread.Btn_Handler.connect(self.Button_Handler)
                self.servoVerticalThread.Btn_Handler.connect(self.Button_Handler)
                self.servoHorizontalThread.horizontal_Sig.connect(self.servo_Handler)
                self.servoVerticalThread.vertical_Sig.connect(self.servo_Handler)
                
        # Resets button if button is pressed while recording video
        def Button_Handler(self, string):
                self.RstBtn = string
                
                if self.RstBtn == "Capture":
                        self.captureBtn.setIcon(QIcon(Camera_Idle_Path))
                        
                elif self.RstBtn == "Record":     
                        self.recordBtn.setIcon(QIcon(Video_Idle_Path))
                        
                elif self.RstBtn == "TimeLapse":
                        self.timelapseBtn.setIcon(QIcon(TimeLapse_Idle_Path))           
                        
                elif self.RstBtn == "ProgressBar":
                        self.PBar.setValue(0)           
                        
                elif self.RstBtn == "Stream":
                        self.Video_Stream.Set_Video_Stream_Ready(True)          
                        
                elif self.RstBtn == "Left":
                        pass
                        #~ print ("Left done")         
                        
                elif self.RstBtn == "Right":
                        pass
                        #~ print ("Right done")           
                        
                elif self.RstBtn == "Up":
                        pass
                        #~ print ("Up done")           
                        
                elif self.RstBtn == "Down":
                        pass
                        #~ print ("Down done")           
                        
        # To put servo value to status bar 
        def servo_Handler(self, string, value):
                if string == 'horizontalMotor':
                        if value == 'Min':
                                self.statusBar.showMessage("Max RIGHT Movement Reached!", 2000) 
                        
                        elif value =='Max':
                                self.statusBar.showMessage("Max LEFT Movement Reached!", 2000) 
                        else:
                                newVal = 180 - int(value)
                                self.xPos.setText("| X: " + str(newVal))
                        
                elif string == 'verticalMotor':
                        if value == 'Min':
                                self.statusBar.showMessage("Max UP Movement Reached!", 2000) 
                        
                        elif value =='Max':
                                self.statusBar.showMessage("Max DOWN Movement Reached!", 2000) 
                        else:
                                newVal = 180 - int(value)
                                self.yPos.setText("| Y: " + str(newVal))

        
# Class to display error messages
class Error_Handler(QObject):
        def __init__(self, consoleLog, captureThre, recordThre, timelapseThre, videoStreamThre, dropDownThre, webStreamThre, statusBar):
                super(Error_Handler, self).__init__()
                self.large_textbox = consoleLog
                self.captureThread = captureThre
                self.recordThread = recordThre
                self.timelapseThread = timelapseThre
                self.videoStream = videoStreamThre
                self.dropDown = dropDownThre
                self.Web_Stream = webStreamThre
                self.statusBar = statusBar
                
                # Connect signals to error function
                self.recordThread.Error_Signal.connect(self.Show_Error)
                self.timelapseThread.Error_Signal.connect(self.Show_Error)
                self.captureThread.Error_Signal.connect(self.Show_Error)
                self.videoStream.Error_Signal.connect(self.Show_Error)
                self.dropDown.Error_Signal.connect(self.Show_Error)
                self.dropDown.Reset_Signal.connect(self.resetAllStreams)
                
        # Function to write error message to console log
        def Show_Error(self, string):
                self.errorMessage = string
                self.statusBar.setStyleSheet(GUI_Style.statusBarRed)
                self.statusBar.showMessage(self.errorMessage, 5000) 
                
        # Function to continue streams after any errors
        def resetAllStreams(self, string):
                self.videoStream.Set_Video_Stream_Ready(True)
                self.Web_Stream.setStart(True)
                
        # Function call to write to Console Log
        def WriteToConsole(self, new_input):
                self.old_window = self.large_textbox.toPlainText()
                self.new_window = self.old_window + '\n' + new_input
                self.large_textbox.setText(self.new_window)
                self.large_textbox.moveCursor(QTextCursor.End)
                

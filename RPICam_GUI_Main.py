import datetime
import os
import time
import sys
import PyQt5
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLineEdit, QLabel, QCheckBox, QTextEdit, QStatusBar,QProgressBar, QSizePolicy, QAbstractItemView, QWidget, QTabWidget, QHBoxLayout, QVBoxLayout, QSlider
from PyQt5.QtGui import QPixmap, QIcon, QFont, QTextCursor, QPalette, QImage, QBrush, QImage
from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot, QObject, QSize

#Imports from made files
from Initialize_PiCam import Setup_PiCam
from RPICam_GUI_Buttons import Snapshot_Button, Record_Button, TimeLapse_Button, Stop_Button, Logo_Button
from RPICam_GUI_Servo import MouseTracker, Left_Button, Right_Button, Up_Button, Down_Button
from RPICam_GUI_Settings import WebStream_Button, Brightness_Slider, Contrast_Slider, Sharpness_Slider, Saturation_Slider, Annotation_Slider, Image_Effect_DropDown, Exposure_Mode_DropDown, Resolution_Framerate_DropDown

from RPI_Capture_Thread import QRPICaptureThread
from RPI_Record_Thread import QRPIRecordVideoThread, QPBarThread
from RPI_TimeLapse_Thread import QRPITimeLapseThread
#~ from RPI_StreamThread import QRPIVideoStreamThread
from RPI_StreamThreadv2 import QRPIVideoStreamThread
from RPI_Slider_Thread import QSliderThread
from RPI_DropDown_Thread import QDropDownThread
from Sleeper_Thread import QTimeThread
from web_stream import WebStream_Thread
from GUI_Stylesheets import GUI_Stylesheets
from RPI_Servo import Initialize_Servo, QServoTrackPadThread, QServoHorizontalThread, QServoVerticalThread

# Current version of application - Update for new builds
appVersion = "2.1"      # Update version

#Initial postion of servos
horizontal_pos = 90
vertical_pos = 90

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

# Create folders for pictures/ videos
Image_Path = Main_path + "Snapshots/"
Video_Path = Main_path + "Videos/"
TimeLapse_Path = Main_path + "Time_Lapse/"

if not os.path.exists(Image_Path):
    os.makedirs(Image_Path)
    
if not os.path.exists(Video_Path):
    os.makedirs(Video_Path)
    
if not os.path.exists(TimeLapse_Path):
    os.makedirs(TimeLapse_Path)
    
    
# Instantiate style sheets for GUI Objects
GUI_Style = GUI_Stylesheets()

# GUI Class to display camera feed on GUI
class Stream_Video(QLabel):             
        
    def __init__(self, window, video_stream, Record_Thread, Capture_Thread, TimeLapse_Thread):
        super(Stream_Video, self).__init__()
        self.setParent(window)
        self.RPI_GUIStream = video_stream
        self.recordThread = Record_Thread
        self.captureThread = Capture_Thread
        self.timelapseThread = TimeLapse_Thread
        
        # Connecting thread (emits) to functions
        self.RPI_GUIStream.Video_Stream_signal.connect(self.StreamToGUI)
        self.captureThread.Send_Image_signal.connect(self.ImagetoGUI)
        self.recordThread.Rec_GUI_signal.connect(self.RecordtoGUI)
        self.timelapseThread.Time_Lapse_Signal.connect(self.TimeLapsetoGUI)
        
    def StreamToGUI(self, input_video):
        self.video_input = input_video
        #~ pixmap = QPixmap(self.video_input)
        #~ self.setPixmap(pixmap)
        
    def ImagetoGUI(self, input_pic):
        pixmap = QPixmap(input_pic)
        self.setPixmap(pixmap)
        
    def RecordtoGUI(self, input_rec):
        pixmap = QPixmap(input_rec)
        self.setPixmap(pixmap)  
             
    def TimeLapsetoGUI(self, input_tlapse):
        pixmap = QPixmap(input_tlapse)
        self.setPixmap(pixmap)       
        
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
                

                
# This will create the main window on the screen
class Window(QMainWindow):
    
    # Initialization of the GUI
    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(50,50,1200,700)
        self.setWindowTitle("RPI Cam v" + appVersion)
        self.setStyleSheet(GUI_Style.NM_mainWindow)
        self.setWindowIcon(QIcon(Icon_Path))
        
        # Initialize Pi Camera for all threads
        PiCam = Setup_PiCam()
        self.camera, self.rawCapture = PiCam.PiCam_Configuration() 
        
        # Initialize Servo for PiCamera
        PiServo = Initialize_Servo()
        self.upDownMotor = PiServo.upDownMotor
        self.leftRightMotor = PiServo.leftRightMotor
        
        # Initalize at center position
        self.leftRightMotor.angle = horizontal_pos
        self.upDownMotor.angle = vertical_pos

        # Create Threads
        self.RPICaptureThread = QRPICaptureThread(self.camera)
        self.RPIRecordThread = QRPIRecordVideoThread(self.camera)
        self.RPITimeLapseThread = QRPITimeLapseThread(self.camera)
        self.Video_Stream = QRPIVideoStreamThread(self.camera, self.rawCapture)
        self.Web_Stream =  WebStream_Thread(self.camera)
        self.Timer_Thread = QTimeThread()
        self.PBarThread = QPBarThread(self.RPIRecordThread)
        self.sliderThread = QSliderThread(self.camera)
        self.dropdownThread = QDropDownThread(self.camera)
        self.servoTrackpadThread = QServoTrackPadThread(PiServo, horizontal_pos, vertical_pos)
        self.leftRightServoThread = QServoHorizontalThread(PiServo, horizontal_pos, vertical_pos)
        self.upDownServoThread = QServoVerticalThread(PiServo, horizontal_pos, vertical_pos)
        
        # Start run() function on threads
        self.RPICaptureThread.start()
        self.RPIRecordThread.start()
        self.RPITimeLapseThread.start()
        self.Video_Stream.start()
        self.Timer_Thread.start()
        self.PBarThread.start()
        self.Web_Stream.start()
        self.sliderThread.start()
        self.dropdownThread.start()
        self.servoTrackpadThread.start()
        self.leftRightServoThread.start()
        self.upDownServoThread.start()
    
        # Start Web server at start up
        self.Web_Stream.StartStreaming(True)
        self.Web_Stream.setStop(True)
        self.Web_Stream.setStart(False)


        # This builds the main widget for the GUI window to hold
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        # Create Tabs
        self.MyTabs = QTabWidget()
        self.MyTabs.setStyleSheet(GUI_Style.tabs)
        self.MyTabs.setMaximumWidth(400)
        
        self.MainTab = QWidget()
        self.SettingsTab = QWidget()
        self.ServoFreelookTab = QWidget()
        self.ServoSliderTab = QWidget()
        self.ServoControllerTab = QWidget()
        
        # Add Tabs and Tab Icon to tab widget
        self.MyTabs.addTab(self.MainTab, QIcon(Main_Tab_Path), '')
        self.MyTabs.addTab(self.ServoFreelookTab, QIcon(Freelook_Path), '') 
        self.MyTabs.addTab(self.ServoControllerTab, QIcon(ServoController_Tab_Path), '') 
        self.MyTabs.addTab(self.SettingsTab,QIcon(Settings_Tab_Path), '')   
        self.MyTabs.setIconSize(QSize(30, 40))
        
        '''Status Bar'''
        # Create bottom Status Bar
        self.StatusBar()
        self.setStatusBar(self.statusBar)
        
        # Create Main window layout to hold tabs and GUI objects
        Main_Window_HLayout = QHBoxLayout()  
        Main_Title_Layout   = QHBoxLayout()  
        Main_Window_VLayout = QVBoxLayout()  
        
        # Instantiate Window objects
        self.VideoStream()
        #~ self.Progress_Bar()
        self.MessageWindowTextBox()
        self.MainLogoButton()
        self.MainTitle()
        
        # Add title and logo to layout
        Main_Title_Layout.addWidget(self.Logo_btn)
        Main_Title_Layout.addWidget(self.UpperText, 0, Qt.AlignCenter)
        Main_Title_Layout.setSpacing(10)
        
        # Add GUI object to left side of GUI window
        Main_Window_VLayout.addLayout(Main_Title_Layout)
        Main_Window_VLayout.addWidget(self.MyTabs) 
        Main_Window_VLayout.addWidget(self.LargeTextBox)
        #~ Main_Window_VLayout.addWidget(self.PBar)
        Main_Window_VLayout.setSpacing(20)
        
        # Add tabs and video stream to main window layout
        Main_Window_HLayout.addLayout(Main_Window_VLayout)       
        Main_Window_HLayout.addWidget(self.Vid_Stream)       
        Main_Window_HLayout.setSpacing(20)     
        Main_Window_HLayout.setContentsMargins(20, 20, 20, 20)    
                
        ''' Home Tab '''
        # Instantiate Home GUI Objects
        self.Snapshot_Btn_GUI()
        self.Progress_Bar()
        self.Record_Btn_GUI()
        self.TimeLapse_Btn_GUI()
        self.Stop_Btn_GUI()
        
        # Create Layout to go on Main tab
        #~ horizontal_stream_layout = QHBoxLayout()  
        vertical_button_layout = QVBoxLayout() 
        
        # Add buttons, console log and progress bar to layout
        vertical_button_layout.addWidget(self.snpsht_btn, 0, Qt.AlignCenter)
        vertical_button_layout.addWidget(self.rec_btn, 0, Qt.AlignCenter) 
        vertical_button_layout.addWidget(self.Time_Lapse_btn, 0, Qt.AlignCenter) 
        vertical_button_layout.addWidget(self.stp_rec_btn, 0, Qt.AlignCenter)
        vertical_button_layout.addWidget(self.PBar)
        vertical_button_layout.setSpacing(30)
        vertical_button_layout.setContentsMargins(0, 20, 0, 0)

        # Add home vertical layout to main tab layout
        self.MainTab.setLayout(vertical_button_layout)
    
        '''Freelook Tab'''
        # Instantiate Servo GUI Objects 
        self.mouseTracker()
        
        # Create Layout to go on frelook Tab
        vertical_servo_layout = QVBoxLayout()
        vertical_servo_layout.addWidget(self.mouseTracker)

        # Add layout to frelook tab 
        self.ServoFreelookTab.setLayout(vertical_servo_layout)
    
        '''Servo Controller Tab'''
        # Instantiate control buttons for Servo Controller Tab
        self.leftButton()
        self.rightButton()
        self.upButton()
        self.downButton()
        
        # Create Layout to go on servo controller Tab
        vertical_servoCtrl_layout = QVBoxLayout()
        horizontal_servoCtrl_layout = QHBoxLayout()
        
        # Add left/ right buttons to horizontal tab
        horizontal_servoCtrl_layout.addWidget(self.left_btn) 
        horizontal_servoCtrl_layout.addWidget(self.right_btn)
        horizontal_servoCtrl_layout.setSpacing(0)
        horizontal_servoCtrl_layout.setContentsMargins(0, 0, 0, 0)
        
        # Add Up, left/ right, down button to one layout
        vertical_servoCtrl_layout.addWidget(self.up_btn)
        vertical_servoCtrl_layout.addLayout(horizontal_servoCtrl_layout)
        vertical_servoCtrl_layout.addWidget(self.down_btn)
        vertical_servoCtrl_layout.setSpacing(0)
        vertical_servoCtrl_layout.setContentsMargins(0, 0, 0, 0)

        # Add servo control layout to servo tab 
        self.ServoControllerTab.setLayout(vertical_servoCtrl_layout)

        
        ''' Settings Tab '''
        # Instantiate Settings GUI Objects    
        self.webStream_Btn_GUI()    
        self.brightnessLabel()
        self.brightnessNumber()
        self.brightnessSlider()
        
        self.contrastLabel()
        self.contrastNumber()
        self.contrastSlider()
        
        self.sharpnessLabel()
        self.sharpnessNumber()
        self.sharpnessSlider()
        
        self.saturationLabel()
        self.saturationNumber()
        self.saturationSlider()
        
        self.annotationLabel()
        self.annotationNumber()
        self.annotationSlider()
        
        self.imageEffectLabel()
        self.ImgEffect_DrpDwn()
        
        self.exposureModeLabel()
        self.exposureMode_DrpDwn()
        
        self.resolutionFramerateLabel()
        self.resolutionFramerate_DrpDwn()
        
        # Create Layout to go on Setting Tab
        horizontal_settings_layout = QHBoxLayout()
        vertical_settings_layout = QVBoxLayout()
        left_VLayout = QVBoxLayout()
        center_VLayout = QVBoxLayout()
        right_VLayout = QVBoxLayout()
        
        left_DrpDwnLayout = QVBoxLayout()
        Right_DrpDwnLayout = QVBoxLayout()
        comboBox_HLayout = QHBoxLayout()
        
        # Left side of slider settings layout
        left_VLayout.addWidget(self.brightnessLbl)
        left_VLayout.addWidget(self.contrastLbl)
        left_VLayout.addWidget(self.sharpnessLbl)
        left_VLayout.addWidget(self.saturationLbl)
        left_VLayout.addWidget(self.annotationLbl)
        left_VLayout.setSpacing(40)
        left_VLayout.setContentsMargins(0, 0, 0, 0)
        
        # Center side of slider settings layout
        center_VLayout.addWidget(self.brightnessNum)
        center_VLayout.addWidget(self.contrastNum)
        center_VLayout.addWidget(self.sharpnessNum)
        center_VLayout.addWidget(self.saturationNum)
        center_VLayout.addWidget(self.annotationNum)
        center_VLayout.setSpacing(40)
        center_VLayout.setContentsMargins(0, 0, 0, 0)
        
        # Right side of slider settings layout
        right_VLayout.addWidget(self.brightnessSldr)
        right_VLayout.addWidget(self.contrastSldr)
        right_VLayout.addWidget(self.sharpnessSldr)
        right_VLayout.addWidget(self.saturationSldr)
        right_VLayout.addWidget(self.annotationSldr)
        right_VLayout.setSpacing(40)
        right_VLayout.setContentsMargins(0, 0, 0, 0)
        
        # add slider layouts to horizontal layout
        horizontal_settings_layout.addLayout(left_VLayout)
        horizontal_settings_layout.addLayout(center_VLayout)
        horizontal_settings_layout.addLayout(right_VLayout)
        horizontal_settings_layout.setSpacing(20)
        horizontal_settings_layout.setContentsMargins(0, 0, 0, 0)
        
        # Add label to left side of combox box layout
        left_DrpDwnLayout.addWidget(self.resFrmrtLbl)
        left_DrpDwnLayout.addWidget(self.imageEffectLbl)
        left_DrpDwnLayout.addWidget(self.exposureModeLbl)
        
        # Add QComboBox to right side of combox box layout
        Right_DrpDwnLayout.addWidget(self.resFrmrtDrpDwn)
        Right_DrpDwnLayout.addWidget(self.imgEffectDrpDwn)
        Right_DrpDwnLayout.addWidget(self.expMdeDrpDwn)
        
        # Add combo box label and GUI object to horizontal layout
        comboBox_HLayout.addLayout(left_DrpDwnLayout)
        comboBox_HLayout.addLayout(Right_DrpDwnLayout)
        comboBox_HLayout.setSpacing(30)
        comboBox_HLayout.setContentsMargins(0, 20, 0, 0)
        
        # add horizontal layouts to vertical layout
        vertical_settings_layout.addWidget(self.webStream_Btn)
        vertical_settings_layout.addLayout(horizontal_settings_layout)
        vertical_settings_layout.addLayout(comboBox_HLayout)
        vertical_settings_layout.setSpacing(10)
        vertical_settings_layout.setContentsMargins(0, 10, 0, 0)
        
        # Add vertical layout to settings tab layout
        self.SettingsTab.setLayout(vertical_settings_layout)    

        # Instantiate button reset handler and error handler
        self.allHandlers()

        '''Add all tabs to GUI'''
        # Set Main window layout to GUI central Widget
        self.centralWidget().setLayout(Main_Window_HLayout)
        self.centralWidget().isWindow()
        
        # start streaming video on start up
        self.Video_Stream.Set_Video_Stream_Ready(True)
        self.Logo_btn.Un_Click()
        
        # Display GUI Objects
        self.show()
        
        
# Function for camera servo controls via keyboard keys
    def keyPressEvent(self, event):
        key = event.key()
 
        if key == Qt.Key_W:     # Move Up
                self.up_btn.On_Click()        
                        
        elif key == Qt.Key_A:   # Move Left
                self.left_btn.On_Click()        
                        
        elif key == Qt.Key_S:   # Move Down
                self.down_btn.On_Click()        
                        
        elif key == Qt.Key_D:   # Move Right
                self.right_btn.On_Click()        
        
    ''' Main Window GUI Objects'''
    # Create Main Title Text
    def MainTitle(self):
        self.UpperText = QLabel(self)
        self.UpperText.setText("RPI Cam Controller")
        self.UpperText.setStyleSheet(GUI_Style.mainTitle)
        
    # Create Main Logo Button
    def MainLogoButton(self):
        self.Logo_btn = Logo_Button(self, "", self.LargeTextBox, self.statusBar, self.xHorizontal, self.yVertical, self.res, self.LargeTextBox)
        self.Logo_btn.setStyleSheet(GUI_Style.startButton)
        self.Logo_btn.pressed.connect(self.Logo_btn.On_Click)
        self.Logo_btn.released.connect(self.Logo_btn.Un_Click)
        self.Logo_btn.setIcon(QIcon(Logo_Path))
        self.Logo_btn.setIconSize(QSize(65, 70))

    # Create Window to stream live feed
    def VideoStream(self):
        self.Vid_Stream = Stream_Video(self, self.Video_Stream, self.RPIRecordThread, self.RPICaptureThread, self.RPITimeLapseThread)
        self.Vid_Stream.setMinimumSize(800, 480)
        self.Vid_Stream.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.Vid_Stream.setBackgroundRole(QPalette.Base)
        self.Vid_Stream.setScaledContents(True)
        self.Vid_Stream.setStyleSheet(GUI_Style.videoStream)

    # Create large textbox
    def MessageWindowTextBox(self):
        self.LargeTextBox = QTextEdit(self)
        self.LargeTextBox.setMaximumHeight(100)
        self.LargeTextBox.setStyleSheet(GUI_Style.consoleLog)
        self.LargeTextBox.setText("Console Log")
        self.LargeTextBox.setReadOnly(True)
        self.LargeTextBox.setLineWrapMode(True)
        self.LargeTextBox.setAlignment(Qt.AlignTop)

    # Create Progress Bar
    def Progress_Bar(self):
        self.PBar = QProgressBar(self)
        self.PBar.setGeometry(75,600,250,25)
        self.PBar.setStyleSheet(GUI_Style.progressBar)
        self.PBar.setTextVisible(True)
        self.PBar.setAlignment(Qt.AlignCenter)
        
        '''Status Bar Objects'''
        # Create Status Bar
    def StatusBar(self):
        self.statusBar = QStatusBar()
        self.statusBar.setStyleSheet(GUI_Style.statusBarWhite)
        
        self.xHorizontal = QLabel()
        self.xHorizontal.setMinimumSize(50, 12)
        self.xHorizontal.setStyleSheet(GUI_Style.statusBar_XY)
        self.xHorizontal.setText("| X: 90")
        self.xHorizontal.setAlignment(Qt.AlignCenter)
        
        self.yVertical = QLabel()
        self.yVertical.setMinimumSize(50, 12)
        self.yVertical.setStyleSheet(GUI_Style.statusBar_XY)
        self.yVertical.setText("| Y: 90")
        self.yVertical.setAlignment(Qt.AlignCenter)
        
        self.res = QLabel()
        self.res.setMinimumSize(50, 15)
        self.res.setStyleSheet(GUI_Style.statusBar_widgets)
        self.res.setText("| res 1280x720")
        self.res.setAlignment(Qt.AlignCenter)
        
        self.statusBar.addPermanentWidget(self.xHorizontal, 0)
        self.statusBar.addPermanentWidget(self.yVertical, 0)
        self.statusBar.addPermanentWidget(self.res, 0)
        
        self.statusBar.showMessage("Starting Up... ", 4000)
        
    ''' Home Tab GUI Objects'''
    # Creating button for snapshots
    def Snapshot_Btn_GUI(self):
        self.snpsht_btn = Snapshot_Button(self, "", self.LargeTextBox, self.RPICaptureThread, self.Video_Stream, self.Timer_Thread, self.RPIRecordThread, self.RPITimeLapseThread)
        self.snpsht_btn.setStyleSheet(GUI_Style.startButton)
        self.snpsht_btn.pressed.connect(self.snpsht_btn.On_Click)
        self.snpsht_btn.released.connect(self.snpsht_btn.Un_Click)
        self.snpsht_btn.setIcon(QIcon(Camera_Idle_Path))
        self.snpsht_btn.setIconSize(QSize(65, 70))

    # Creating button for recording video
    def Record_Btn_GUI(self):
        self.rec_btn = Record_Button(self, "", self.LargeTextBox, self.RPIRecordThread, self.PBar, self.Video_Stream, self.PBarThread, self.RPICaptureThread, self.RPITimeLapseThread, self.Timer_Thread)
        self.rec_btn.setStyleSheet(GUI_Style.recordButton)
        self.rec_btn.pressed.connect(self.rec_btn.On_Click)
        self.rec_btn.released.connect(self.rec_btn.Un_Click)
        self.rec_btn.setIcon(QIcon(Video_Idle_Path))
        self.rec_btn.setIconSize(QSize(80, 80))
        
    # Creating button for recording video
    def TimeLapse_Btn_GUI(self):
        self.Time_Lapse_btn = TimeLapse_Button(self, "", self.LargeTextBox, self.Video_Stream, self.RPIRecordThread, self.RPICaptureThread, self.RPITimeLapseThread, self.Timer_Thread, self.snpsht_btn)
        self.Time_Lapse_btn.setStyleSheet(GUI_Style.timelapseButton)
        self.Time_Lapse_btn.pressed.connect(self.Time_Lapse_btn.On_Click)
        self.Time_Lapse_btn.released.connect(self.Time_Lapse_btn.Un_Click)
        self.Time_Lapse_btn.setIcon(QIcon(TimeLapse_Idle_Path))
        self.Time_Lapse_btn.setIconSize(QSize(60, 60))

    # Creating button for recording video
    def Stop_Btn_GUI(self):
        self.stp_rec_btn = Stop_Button(self, "", self.LargeTextBox, self.RPIRecordThread, self.rec_btn, self.Video_Stream, self.PBarThread, self.RPICaptureThread, self.RPITimeLapseThread)
        self.stp_rec_btn.setStyleSheet(GUI_Style.stopButton)
        self.stp_rec_btn.pressed.connect(self.stp_rec_btn.On_Click)
        self.stp_rec_btn.released.connect(self.stp_rec_btn.Un_Click) 
        self.stp_rec_btn.setIcon(QIcon(Stop_Idle_Path))
        self.stp_rec_btn.setIconSize(QSize(60, 60))

    '''Handler classes'''
    # Instantiate button handler object class
    def allHandlers(self):
        self.buttonHandler = Button_Reset_Handler(self.RPICaptureThread, self.RPIRecordThread, self.RPITimeLapseThread, self.PBarThread, 
                                                        self.snpsht_btn, self.rec_btn, self.Time_Lapse_btn,self.PBar, self.Video_Stream, 
                                                        self.leftRightServoThread, self.upDownServoThread , self.statusBar, self.xHorizontal, 
                                                        self.yVertical)
        self.errorHandler = Error_Handler(self.LargeTextBox, self.RPICaptureThread, self.RPIRecordThread, self.RPITimeLapseThread, 
                                                        self.Video_Stream, self.dropdownThread, self.Web_Stream, self.statusBar)

    ''' Settings Tab GUI Objects'''
    # Start web stream button
    def webStream_Btn_GUI(self):
        self.webStream_Btn = WebStream_Button(self, "Start Web Stream", self.LargeTextBox, self.Web_Stream)
        self.webStream_Btn.setStyleSheet(GUI_Style.webButton)
        self.webStream_Btn.pressed.connect(self.webStream_Btn.On_Click)
        self.webStream_Btn.released.connect(self.webStream_Btn.Un_Click) 
        #~ self.webStream_Btn.setIcon(QIcon(Stop_Idle_Path))
        #~ self.webStream_Btn.setIconSize(QSize(60, 60))
        #~ self.webStream_Btn.setSize(60, 60)
    
    # Brightness text/ logo
    def brightnessLabel(self):
        self.brightnessLbl = QLabel(self)
        self.brightnessLbl.setText("Brightness:")
        self.brightnessLbl.setStyleSheet(GUI_Style.sliderLabel)   
      
    # Brightness Slider QLabel to show current number 
    def brightnessNumber(self):
        self.brightnessNum = QLabel(self)
        self.brightnessNum.setMaximumWidth(40)
        self.brightnessNum.setText("50")
        self.brightnessNum.setStyleSheet(GUI_Style.sliderNumber)       
           
    # Brightness Slider
    def brightnessSlider(self):
        self.brightnessSldr = Brightness_Slider(self, self.brightnessNum, self.sliderThread)
        self.brightnessSldr.setOrientation(Qt.Horizontal)
        self.brightnessSldr.setStyleSheet(GUI_Style.brightnessSlider)     
        self.brightnessSldr.setFocusPolicy(Qt.NoFocus)
        self.brightnessSldr.setRange(0, 100)
        self.brightnessSldr.setValue(50)
        self.brightnessSldr.valueChanged[int].connect(self.brightnessSldr.changeValue)
        
    # Contrast text/ logo
    def contrastLabel(self):
        self.contrastLbl = QLabel(self)
        self.contrastLbl.setText("Contrast:")
        self.contrastLbl.setStyleSheet(GUI_Style.sliderLabel)   
           
    # Contrast Slider QLabel to show current number 
    def contrastNumber(self):
        self.contrastNum = QLabel(self)
        self.contrastNum.setMaximumWidth(40)
        self.contrastNum.setText("0")
        self.contrastNum.setStyleSheet(GUI_Style.sliderNumber)  
           
    # Contrast Slider
    def contrastSlider(self):
        self.contrastSldr = Contrast_Slider(self, self.contrastNum, self.sliderThread)
        self.contrastSldr.setOrientation(Qt.Horizontal)
        self.contrastSldr.setStyleSheet(GUI_Style.contrastSlider)  
        self.contrastSldr.setFocusPolicy(Qt.NoFocus)
        self.contrastSldr.setRange(-100, 100)
        self.contrastSldr.valueChanged[int].connect(self.contrastSldr.changeValue)
        
    # Sharpness text/ logo
    def sharpnessLabel(self):
        self.sharpnessLbl = QLabel(self)
        self.sharpnessLbl.setText("Sharpness:")
        self.sharpnessLbl.setStyleSheet(GUI_Style.sliderLabel)   
           
    # Sharpness Slider QLabel to show current number 
    def sharpnessNumber(self):
        self.sharpnessNum = QLabel(self)
        self.sharpnessNum.setMaximumWidth(40)
        self.sharpnessNum.setText("0")
        self.sharpnessNum.setStyleSheet(GUI_Style.sliderNumber) 
        
    # Sharpness Slider
    def sharpnessSlider(self):
        self.sharpnessSldr = Sharpness_Slider(self, self.sharpnessNum, self.sliderThread)
        self.sharpnessSldr.setOrientation(Qt.Horizontal)
        self.sharpnessSldr.setStyleSheet(GUI_Style.sharpnessSlider)       
        self.sharpnessSldr.setFocusPolicy(Qt.NoFocus)
        self.sharpnessSldr.setRange(-100, 100)       
        self.sharpnessSldr.valueChanged[int].connect(self.sharpnessSldr.changeValue)
            
    # Saturation text/ logo
    def saturationLabel(self):
        self.saturationLbl = QLabel(self)
        self.saturationLbl.setText("Saturation:")
        self.saturationLbl.setStyleSheet(GUI_Style.sliderLabel)   
           
    # Saturation Slider QLabel to show current number 
    def saturationNumber(self):
        self.saturationNum = QLabel(self)
        self.saturationNum.setMaximumWidth(40)
        self.saturationNum.setText("0")
        self.saturationNum.setStyleSheet(GUI_Style.sliderNumber) 
        
    # Saturation Slider
    def saturationSlider(self):
        self.saturationSldr = Saturation_Slider(self, self.saturationNum, self.sliderThread)
        self.saturationSldr.setOrientation(Qt.Horizontal)
        self.saturationSldr.setStyleSheet(GUI_Style.saturationSlider)  
        self.saturationSldr.setFocusPolicy(Qt.NoFocus)
        self.saturationSldr.setRange(-100, 100)
        self.saturationSldr.valueChanged[int].connect(self.saturationSldr.changeValue)
        
    # Annotation text/ logo
    def annotationLabel(self):
        self.annotationLbl = QLabel(self)
        self.annotationLbl.setText("Annotation Size:")
        self.annotationLbl.setStyleSheet(GUI_Style.sliderLabel)   
           
    # Annotation Slider QLabel to show current number 
    def annotationNumber(self):
        self.annotationNum = QLabel(self)
        self.annotationNum.setMaximumWidth(40)
        self.annotationNum.setText("30")
        self.annotationNum.setStyleSheet(GUI_Style.sliderNumber) 
        
    # Annotation Slider
    def annotationSlider(self):
        self.annotationSldr = Annotation_Slider(self, self.annotationNum, self.sliderThread)
        self.annotationSldr.setOrientation(Qt.Horizontal)
        self.annotationSldr.setStyleSheet(GUI_Style.annotationSlider)
        self.annotationSldr.setFocusPolicy(Qt.NoFocus)
        self.annotationSldr.setRange(6, 160)
        self.annotationSldr.setValue(30)
        self.camera.annotate_text_size = 30
        self.annotationSldr.valueChanged[int].connect(self.annotationSldr.changeValue)
        
    # Image Effect text/ logo
    def imageEffectLabel(self):
        self.imageEffectLbl = QLabel(self)
        self.imageEffectLbl.setText("Image Effect:")
        self.imageEffectLbl.setStyleSheet(GUI_Style.sliderLabel)   
   
    # To create a drop down for image effect
    def ImgEffect_DrpDwn(self):
        self.imgEffectDrpDwn = Image_Effect_DropDown(self, self.LargeTextBox, self.dropdownThread)
        self.imgEffectDrpDwn.addItem("none")
        self.imgEffectDrpDwn.addItem("negative")
        self.imgEffectDrpDwn.addItem("solarize")
        self.imgEffectDrpDwn.addItem("sketch")
        self.imgEffectDrpDwn.addItem("denoise")
        self.imgEffectDrpDwn.addItem("emboss")
        self.imgEffectDrpDwn.addItem("oilpaint")
        self.imgEffectDrpDwn.addItem("hatch")
        self.imgEffectDrpDwn.addItem("gpen")
        self.imgEffectDrpDwn.addItem("pastel")
        self.imgEffectDrpDwn.addItem("watercolor")
        self.imgEffectDrpDwn.addItem("film")
        self.imgEffectDrpDwn.addItem("blur")
        self.imgEffectDrpDwn.addItem("saturation")
        self.imgEffectDrpDwn.addItem("colorswap")
        self.imgEffectDrpDwn.addItem("washedout")
        self.imgEffectDrpDwn.addItem("posterise")
        self.imgEffectDrpDwn.addItem("colorpoint")
        self.imgEffectDrpDwn.addItem("colorbalance")
        self.imgEffectDrpDwn.addItem("cartoon")
        self.imgEffectDrpDwn.addItem("deinterlace1")
        self.imgEffectDrpDwn.addItem("deinterlace2")
        self.imgEffectDrpDwn.setStyleSheet(GUI_Style.imageEffect)
        self.imgEffectDrpDwn.activated[str].connect(self.imgEffectDrpDwn.ImageEffect_Selection)
        
    # Exposure Mode text/ logo
    def exposureModeLabel(self):
        self.exposureModeLbl = QLabel(self)
        self.exposureModeLbl.setText("Exposure Mode:")
        self.exposureModeLbl.setStyleSheet(GUI_Style.sliderLabel)   
   
    # To create a drop down for Exposure Mode
    def exposureMode_DrpDwn(self):
        self.expMdeDrpDwn = Exposure_Mode_DropDown(self, self.LargeTextBox, self.dropdownThread)
        self.expMdeDrpDwn.addItem("auto")
        self.expMdeDrpDwn.addItem("off")
        self.expMdeDrpDwn.addItem("night")
        self.expMdeDrpDwn.addItem("nightpreview")
        self.expMdeDrpDwn.addItem("backlight")
        self.expMdeDrpDwn.addItem("spotlight")
        self.expMdeDrpDwn.addItem("sports")
        self.expMdeDrpDwn.addItem("snow")
        self.expMdeDrpDwn.addItem("beach")
        self.expMdeDrpDwn.addItem("verylong")
        self.expMdeDrpDwn.addItem("fixedfps")
        self.expMdeDrpDwn.addItem("antishake")
        self.expMdeDrpDwn.addItem("fireworks")
        self.expMdeDrpDwn.setStyleSheet(GUI_Style.exposureMode)
        self.camera.exposure_mode = "auto"
        self.expMdeDrpDwn.activated[str].connect(self.expMdeDrpDwn.exposureMode_Selection)
        
    # Resolution/ Framerate text/ logo
    def resolutionFramerateLabel(self):
        self.resFrmrtLbl = QLabel(self)
        self.resFrmrtLbl.setText("Resolution/ FPS:")
        self.resFrmrtLbl.setStyleSheet(GUI_Style.sliderLabel)   
   
    # To create a drop down for Exposure Mode
    def resolutionFramerate_DrpDwn(self):
        self.resFrmrtDrpDwn = Resolution_Framerate_DropDown(self, self.LargeTextBox, self.dropdownThread, self.Video_Stream, self.Web_Stream, self.Timer_Thread, self.res)
        self.resFrmrtDrpDwn.addItem("1640x1232 @ 30 fps")
        self.resFrmrtDrpDwn.addItem("1640x922 @ 30 fps")
        self.resFrmrtDrpDwn.addItem("1280x720 @ 40 fps")
        self.resFrmrtDrpDwn.addItem("640x480 @ 60 fps")
        self.resFrmrtDrpDwn.setCurrentIndex(2)

        self.resFrmrtDrpDwn.setStyleSheet(GUI_Style.resolutionFramerate)   
        self.camera.resolution = (1280, 720)
        self.camera.framerate = 60 
        self.resFrmrtDrpDwn.activated[str].connect(self.resFrmrtDrpDwn.resolutionFramerate_Selection)
   
        '''Freelook tab GUI Objects'''   
    # To create a mouse pad for camera freelook
    def mouseTracker(self):
        self.mouseTracker = MouseTracker(self, self.leftRightServoThread, self.upDownServoThread)
        self.mouseTracker.setMaximumSize(360, 340)
        self.mouseTracker.setStyleSheet(GUI_Style.mouseTrackPad)
        self.mouseTracker.setMouseTracking(True)
   
        '''Servo Controller tab GUI Objects'''   
    # To create button for left click events
    def leftButton(self):
        self.left_btn = Left_Button(self, "", self.leftRightServoThread)
        self.left_btn.setStyleSheet(GUI_Style.startButton)
        self.left_btn.clicked.connect(self.left_btn.On_Click)
        self.left_btn.setIcon(QIcon(Left_Button_Path))
        self.left_btn.setIconSize(QSize(65, 70))
        
    # To create button for right click events
    def rightButton(self):
        self.right_btn = Right_Button(self, "", self.leftRightServoThread)
        self.right_btn.setStyleSheet(GUI_Style.startButton)
        self.right_btn.clicked.connect(self.right_btn.On_Click)
        self.right_btn.setIcon(QIcon(Right_Button_Path))
        self.right_btn.setIconSize(QSize(65, 70))
        
    # To create button for up click events
    def upButton(self):
        self.up_btn = Up_Button(self, "", self.upDownServoThread)
        self.up_btn.setStyleSheet(GUI_Style.startButton)
        self.up_btn.clicked.connect(self.up_btn.On_Click)
        self.up_btn.setIcon(QIcon(Up_Button_Path))
        self.up_btn.setIconSize(QSize(65, 70))
        
    # To create button for down click events
    def downButton(self):
        self.down_btn = Down_Button(self, "", self.upDownServoThread)
        self.down_btn.setStyleSheet(GUI_Style.startButton)
        self.down_btn.clicked.connect(self.down_btn.On_Click)
        self.down_btn.setIcon(QIcon(Down_Button_Path))
        self.down_btn.setIconSize(QSize(65, 70))

        
    # Stop all threads when GUI is closed
    def closeEvent(self, *args, **kwargs):
        self.RPICaptureThread.Set_Exit_Program(True)
        self.RPICaptureThread.wait(100)
        self.RPIRecordThread.Set_Exit_Program(True)
        self.RPIRecordThread.wait(100)
        self.RPITimeLapseThread.Set_Exit_Program(True)
        self.RPITimeLapseThread.wait(100)
        self.Video_Stream.Set_Exit_Program(True)
        self.Video_Stream.wait(100)
        self.Timer_Thread.Set_Exit_Program(True)
        self.Timer_Thread.wait(100)
        self.PBarThread.Set_Exit_Program(True)
        self.PBarThread.wait(100)
        self.Web_Stream.Set_Exit_Program(True)
        self.Web_Stream.wait(100)
        self.sliderThread.Set_Exit_Program(True)
        self.sliderThread.wait(100)
        self.dropdownThread.Set_Exit_Program(True)
        self.dropdownThread.wait(100)
        self.servoTrackpadThread.Set_Exit_Program(True)
        self.servoTrackpadThread.wait(100)
        self.leftRightServoThread.Set_Exit_Program(True)
        self.leftRightServoThread.wait(100)
        self.upDownServoThread.Set_Exit_Program(True)
        self.upDownServoThread.wait(100)


#Main loop
def run():
    #Run the application
    app = QApplication(sys.argv)
    #Create GUI
    GUI = Window()
    #Exit
    sys.exit(app.exec())

#Main code
if __name__ == "__main__":
    run()
    
    
# Changelog:
# 0.1 - Initial GUI and RPICam.py modules created - Jan 17, 2019
# 0.2 - Snapshot, record, and stop record buttons completed - Jan 20, 2019
# 0.3 - GUI can display live stream - Jan 23, 2019
# 0.4 - Created .py file to initialize PiCamera and configurations. Live Feed exands as window expands.- Jan 25, 2019
# 0.5 - Created new thread to update progress bar. Updated buttons with Icons - Jan 28, 2019
# 0.6 - Created widget to hold buttons, removed input textbox now video records for 1 min, video recording now displays on GUI Qlabel 
#       Can capture images while video is recording - Jan 29, 2019
# 0.7 - Fix bugs when capturing image while recording. Added main and settings tab. Created Time Lapse Button. 
#       Stop button stops all running procedures and resets stream annotations. Jan 31, 2019
# 0.8 - Bug Fixes. Feb 10, 2019
# 0.9 - Integrated web stream to GUI stream. Feb 13, 2019
# 1.0 - Seperate all thread into different .py files for organization. Complete optimization. Feb 19, 2019
# 1.1 - Added sliders for settings tab. Created seperate .py files for buttons and sliders. 
#       Added customization to QSliders and QComboBox. Feb 22, 2019
# 1.2 - Created seperate .py for all GUI stylesheets for code optimization. Create QComboBox for exposure mode. Feb 25, 2019
# 1.3 - Add try/ exceptions to RPI Button threads for error handling. Timelapse now removes all images taken after video is created. Feb 27, 2019
# 1.4 - Added resolution/ Framerate button. Mar 6, 2019
# 1.5 - Added servo funcationality and tabs for control. Added keyboard keys for control of servos 'WASD' - Mar 11, 2019
# 1.6 - Added status bar located bottom left - Mar 12, 2019
# 1.7 - Added thread for smoother motor movements. Removed Sliders tab - Mar 23, 2019
# 1.8 - Moved starting web stream to a button. Added night secret mode button. - Apr 23, 2019
# 1.9 - Create folder path if not created at start up. - May 2, 2019
# 2.0 - Rewrite stream thread from capture_contnious to capture_sequence, wed stream button fix to start server but disable stream at startup. - July 15, 2019
# 2.1 - Adding Open CV to pi camera for image processing

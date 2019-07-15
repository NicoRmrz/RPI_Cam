import PyQt5
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLineEdit, QLabel, QCheckBox, QTextEdit, QProgressBar, QSizePolicy, QWidget, QTabWidget, QHBoxLayout, QVBoxLayout, QSlider, QComboBox
from PyQt5.QtGui import QPixmap, QIcon, QFont, QTextCursor, QPalette, QImage, QBrush
from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot, QObject, QSize

# User made file
from GUI_Stylesheets import GUI_Stylesheets

# Instantiate style sheets for GUI Objects
GUI_Style = GUI_Stylesheets()

#GUI Classes
# Pushbutton class to enable webStream
class WebStream_Button(QPushButton):         #WebStream button
    def __init__(self, window, text, consoleLog, webThread):
        super(WebStream_Button, self).__init__()
        self.setText(text)
        self.setParent(window)
        self.large_textbox = consoleLog
        self.Web_Stream = webThread
        self.AmIStreaming = False
        self.Web_Stream.setStop(True)

        # Connecting Signals
        self.Web_Stream.Web_Stream_signal.connect(self.Web_Stream_ON)
        
    # Function call for the click event
    def On_Click(self):
        pass
        
    # Function call for the Un_click event
    def Un_Click(self):
        if self.AmIStreaming != True:
            self.setStyleSheet(GUI_Style.webButtonOn)   # Button turns red for activated
            self.Web_Stream.setStart(True)
            self.setText("Streaming")
            self.WriteToConsole("Web Stream URL: 69.4.154.148:7227")  
            self.AmIStreaming  = True
            
        elif self.AmIStreaming != False:
            self.setStyleSheet(GUI_Style.webButton)   # Button turns red for activated
            self.setText("Start Web Stream")
            self.Web_Stream.setStop(True)
            self.WriteToConsole("Web Stream Disabled")             # write web stream disabled 
            self.AmIStreaming = False


    # Funtion call for web stream on acknoledgment
    def Web_Stream_ON(self, string):
            self.WriteToConsole(string)             # write web stream enabled 
                 
    # Function call to write to Console Log
    def WriteToConsole(self, new_input):
            self.old_window = self.large_textbox.toPlainText()
            self.new_window = self.old_window + '\n' + new_input
            self.large_textbox.setText(self.new_window)
            self.large_textbox.moveCursor(QTextCursor.End)
    
        
#This is the class for sliders from the Pyqt 5 framework
class Brightness_Slider(QSlider):         #Brightness Slider

    # Initializes the necessary objects into the slider class for control
    def __init__(self, window, label, thread):
        super(Brightness_Slider, self).__init__()
        self.setParent(window)
        self.currVal = label
        self.thread = thread
        self.thread.brightnessLabel_Sig.connect(self.updateLabel)

    # Function for recieving new value from slider
    def changeValue(self, value):
        self.newValue = value
        self.thread.set_brightnessSlider(True, self.newValue)
        
    # Function to update QLabel for slider value
    def updateLabel(self, value):
        self.value = value
        self.currVal.setText(str(self.value))
        
class Contrast_Slider(QSlider):         #Contrast Slider

    # Initializes the necessary objects into the slider class for control
    def __init__(self, window, label, thread):
        super(Contrast_Slider, self).__init__()
        self.setParent(window)
        self.currVal = label
        self.thread = thread
        self.thread.contrastLabel_Sig.connect(self.updateLabel)

    # Function for recieving new value from slider
    def changeValue(self, value):
        self.newValue = value
        self.thread.set_contrastSlider(True, self.newValue)
        
    # Function to update QLabel for slider value
    def updateLabel(self, value):
        self.value = value
        self.currVal.setText(str(self.value))
        
class Sharpness_Slider(QSlider):         #Sharpness Slider

    # Initializes the necessary objects into the slider class for control
    def __init__(self, window, label, thread):
        super(Sharpness_Slider, self).__init__()
        self.setParent(window)
        self.currVal = label
        self.thread = thread
        self.thread.sharpnessLabel_Sig.connect(self.updateLabel)

    # Function for recieving new value from slider
    def changeValue(self, value):
        self.newValue = value
        self.thread.set_sharpnessSlider(True, self.newValue)
        
    # Function to update QLabel for slider value
    def updateLabel(self, value):
        self.value = value
        self.currVal.setText(str(self.value))
        
class Saturation_Slider(QSlider):         #Saturation Slider

    # Initializes the necessary objects into the slider class for control
    def __init__(self, window, label, thread):
        super(Saturation_Slider, self).__init__()
        self.setParent(window)
        self.currVal = label
        self.thread = thread
        self.thread.saturationLabel_Sig.connect(self.updateLabel)

    # Function for recieving new value from slider
    def changeValue(self, value):
        self.newValue = value
        self.thread.set_saturationSlider(True, self.newValue)
        
    # Function to update QLabel for slider value
    def updateLabel(self, value):
        self.value = value
        self.currVal.setText(str(self.value))
        
class Annotation_Slider(QSlider):         #Annotation Slider

    # Initializes the necessary objects into the slider class for control
    def __init__(self, window, label, thread):
        super(Annotation_Slider, self).__init__()
        self.setParent(window)
        self.currVal = label
        self.thread = thread
        self.thread.annotationLabel_Sig.connect(self.updateLabel)

    # Function for recieving new value from slider
    def changeValue(self, value):
        self.newValue = value
        self.thread.set_annotationSlider(True, self.newValue)
        
    # Function to update QLabel for slider value
    def updateLabel(self, value):
        self.value = value
        self.currVal.setText(str(self.value))
        
class Image_Effect_DropDown(QComboBox):         #Image effect drop down box
    old_window = None
    new_window = None
    
    # Initializes the necessary objects into the QComboBox class for control
    def __init__(self, window, input_largetextbox, dropdownThread):
        super(Image_Effect_DropDown, self).__init__()
        self.setParent(window)
        self.large_textbox = input_largetextbox
        self.dropDownThread = dropdownThread
        
        # Connect signal to function
        self.dropDownThread.imgEffect_Sig.connect(self.Selection_Done)

    # Function call for the click event
    def ImageEffect_Selection(self, sel):
        self.selection = sel
        self.dropDownThread.set_imgEffectReady(True, self.selection)
        
    # Function for when selection is completed   
    def Selection_Done(self, value):
        self.selectionChosen = value
        self.WriteToConsole("Image Effect set to " + self.selectionChosen)
        
    # Function call to write to Console Log
    def WriteToConsole(self, new_input):
        self.old_window = self.large_textbox.toPlainText()
        self.new_window = self.old_window + '\n' + new_input
        self.large_textbox.setText(self.new_window)
        self.large_textbox.moveCursor(QTextCursor.End)
        
class Exposure_Mode_DropDown(QComboBox):         # Exposure Mode drop down box
    old_window = None
    new_window = None
    
    # Initializes the necessary objects into the QComboBox class for control
    def __init__(self, window, input_largetextbox, dropdownThread):
        super(Exposure_Mode_DropDown, self).__init__()
        self.setParent(window)
        self.large_textbox = input_largetextbox
        self.dropDownThread = dropdownThread
        
        # Connect signal to function
        self.dropDownThread.exposureMode_Sig.connect(self.Selection_Done)

    # Function call for the click event
    def exposureMode_Selection(self, sel):
        self.selection = sel
        self.dropDownThread.set_exposureModeReady(True, self.selection)
        
    # Function for when selection is completed   
    def Selection_Done(self, value):
        self.selectionChosen = value
        self.WriteToConsole("Exposure Mode set to " + self.selectionChosen)
        
    # Function call to write to Console Log
    def WriteToConsole(self, new_input):
        self.old_window = self.large_textbox.toPlainText()
        self.new_window = self.old_window + '\n' + new_input
        self.large_textbox.setText(self.new_window)
        self.large_textbox.moveCursor(QTextCursor.End)
        
class Resolution_Framerate_DropDown(QComboBox):         # Resolution/ Framerate drop down box
    old_window = None
    new_window = None
    
    # Initializes the necessary objects into the QComboBox class for control
    def __init__(self, window, input_largetextbox, dropdownThread, guiStream, webStream, timerThre, resStatus):
        super(Resolution_Framerate_DropDown, self).__init__()
        self.setParent(window)
        self.large_textbox = input_largetextbox
        self.dropDownThread = dropdownThread
        self.Video_Stream = guiStream
        self.Web_Stream = webStream
        self.timer = timerThre
        self.resStatus = resStatus
        
        # Connect signal to function
        self.dropDownThread.resFrmrt_Sig.connect(self.Selection_Done)
        self.timer.dropdown_signal.connect(self.set_resolutionFramerate)

    # Function call for the click event
    def resolutionFramerate_Selection(self, sel):
        self.selection = sel
               
        #Stop all stream to change resolution
        self.Video_Stream.Set_Video_Stream_Ready(False)
        self.Web_Stream.setStop(True)
        
        # Timer wait for streams to pause
        self.timer.set_dropDownTimer(1, True)
    
    # Function to set Thread after waiting for streams to pause
    def set_resolutionFramerate(self, string):
        self.dropDownThread.set_resolutionFramerateReady(True, self.selection)
        
    # Function for when selection is completed   
    def Selection_Done(self, resolution, framerate):
        self.resStatus.setText("| res " + resolution)
        self.WriteToConsole("Resolution set to " + resolution) 
        self.WriteToConsole("Framerate set to " + framerate) 
        
        # Continue all Stream
        self.Video_Stream.Set_Video_Stream_Ready(True)
        self.Web_Stream.setStop(False)
        self.Web_Stream.setStart(True)
        #~ self.Web_Stream.StartStreaming(True)
        
    # Function call to write to Console Log
    def WriteToConsole(self, new_input):
        self.old_window = self.large_textbox.toPlainText()
        self.new_window = self.old_window + '\n' + new_input
        self.large_textbox.setText(self.new_window)
        self.large_textbox.moveCursor(QTextCursor.End)
        
   

import os
import sys
import PyQt5
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLineEdit, QLabel, QCheckBox, QToolTip, QTextEdit, QProgressBar, QSizePolicy, QAbstractItemView, QWidget, QTabWidget, QHBoxLayout, QVBoxLayout, QSlider
from PyQt5.QtGui import QPixmap, QIcon, QFont, QTextCursor, QPalette, QImage, QBrush, QCursor
from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot, QObject, QSize

# QT GUI class for the mouse freelook feature for the Pi Camera
class MouseTracker(QLabel):
        def __init__(self):
                super().__init__()
                x = 0
                y = 0
       
        def mouseMoveEvent(self, event):
                x = round(event.x() / 2)
                y = round(event.y() / 2)
                QToolTip.showText(QCursor.pos(), str(x) + "," + str(y))
                #Set thread
                
                        
class Left_Button(QPushButton):
    def __init__(self, window, text, thread):
        super(Left_Button, self).__init__()
        self.setText(text)
        self.setParent(window)
        self.servoThread = thread
        
        #Connecting completions signals to functions
        #~ self.servoThread.left_Sig.connect(self.ButtonDone)    
        
    # Function call for the click event
    def On_Click(self):
        self.servoThread.set_leftButton(True)
        # Button turns yellow for activated
        #~ self.setIcon(QIcon(Camera_Capture_Path))

    # Function call for the Done event
    #~ def ButtonDone(self, value):
        #~ print(value)
        
        # Function call for the Un_click event
    def Un_Click(self):
        #~ self.servoThread.Set_Video_Stream_Ready(False)
        pass
       
        
class Right_Button(QPushButton):
    def __init__(self, window, text, thread):
        super(Right_Button, self).__init__()
        self.setText(text)
        self.setParent(window)
        self.servoThread = thread
        
       #Connecting completions signals to functions
        #~ self.servoThread.right_Sig.connect(self.ButtonDone)    
        
    # Function call for the click event
    def On_Click(self):
        self.servoThread.set_rightButton(True)
        # Button turns yellow for activated
        #~ self.setIcon(QIcon(Camera_Capture_Path))

    # Function call for the Done event
    #~ def ButtonDone(self, value):
        #~ print(value)
        
        # Function call for the Un_click event
    def Un_Click(self):
        #~ self.servoThread.Set_Video_Stream_Ready(False)
        pass
        
class Up_Button(QPushButton):
    def __init__(self, window, text, thread):
        super(Up_Button, self).__init__()
        self.setText(text)
        self.setParent(window)
        self.servoThread = thread
        
        #Connecting completions signals to functions
        #~ self.servoThread.Snap_Captured_signal.connect(self.Snapshot_Captured)    
        
    # Function call for the click event
    def On_Click(self):
        self.servoThread.set_upButton(True)
        #~ print("up button")
        
        # Button turns yellow for activated
        #~ self.setIcon(QIcon(Camera_Capture_Path))

    # Function call for the Un_click event
    def Un_Click(self):
        #~ self.servoThread.Set_Video_Stream_Ready(False)
        pass
        
class Down_Button(QPushButton):
    def __init__(self, window, text, thread):
        super(Down_Button, self).__init__()
        self.setText(text)
        self.setParent(window)
        self.servoThread = thread
        
        #Connecting completions signals to functions
        #~ self.servoThread.Snap_Captured_signal.connect(self.Snapshot_Captured)    
        
    # Function call for the click event
    def On_Click(self):
        self.servoThread.set_downButton(True)
        #~ print("down button")
        
        # Button turns yellow for activated
        #~ self.setIcon(QleftIcon(Camera_Capture_Path))

    # Function call for the Un_click event
    def Un_Click(self):
        #~ self.servoThread.Set_Video_Stream_Ready(False)
        pass
        
                
class upDown_Slider(QSlider):         #Up Down servo Slider

    # Initializes the necessary objects into the slider class for control
    def __init__(self, window, thread):
        super(upDown_Slider, self).__init__()
        self.setParent(window)
        self.thread = thread
        
        # Connect done signal to function
        self.thread.upDown_Sig.connect(self.sliderDone)

    # Function for recieving new value from slider
    def changeValue(self, value):
        self.newValue = str(value)
        QToolTip.showText(QCursor.pos(), self.newValue)
        self.thread.set_upDownSlider(True, value)
        
    # Function for "Done" after slider change
    def sliderDone(self, value):
        #~ print ("Up - Down: ", value)    
        pass
        
        
        
class leftRight_Slider(QSlider):         #Left right servo Slider

    # Initializes the necessary objects into the slider class for control
    def __init__(self, window, thread):
        super(leftRight_Slider, self).__init__()
        self.setParent(window)
        self.thread = thread
        
        # Connect done signal to function
        self.thread.leftRight_Sig.connect(self.sliderDone)

    # Function for recieving new value from slider
    def changeValue(self, value):
        self.newValue = str(value)
        QToolTip.showText(QCursor.pos(), self.newValue)
        self.thread.set_leftRightSlider(True, value)
        
    # Function for "Done" after slider change
    def sliderDone(self, value):
        #~ print ("Left - Right: ", value)
        pass
        


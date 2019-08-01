import os
import sys
import PyQt5
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLineEdit, QLabel, QCheckBox, QToolTip, QTextEdit, QProgressBar, QSizePolicy, QAbstractItemView, QWidget, QTabWidget, QHBoxLayout, QVBoxLayout, QSlider
from PyQt5.QtGui import QPixmap, QIcon, QFont, QTextCursor, QPalette, QImage, QBrush, QCursor
from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot, QObject, QSize

Main_path = os.getcwd() + "/"     
Left_Button_Path = Main_path + 'Icon_Image/leftButton.png'
Right_Button_Path = Main_path + 'Icon_Image/rightButton.png'
Up_Button_Path = Main_path + 'Icon_Image/upButton.png'
Down_Button_Path = Main_path + 'Icon_Image/downButton.png'
Left_Button_Pressed_Path = Main_path + 'Icon_Image/leftButton_Pressed.png'
Right_Button_Pressed_Path = Main_path + 'Icon_Image/rightButton_Pressed.png'
Up_Button_Pressed_Path = Main_path + 'Icon_Image/upButton_Pressed.png'
Down_Button_Pressed_Path = Main_path + 'Icon_Image/downButton_Pressed.png'

# --------------------------------------------------------------------------------------------------------------
# --------------------------------- Mouse Tracker/ Free Look Class ---------------------------------------------
# --------------------------------------------------------------------------------------------------------------
class MouseTracker(QLabel):
        def __init__(self, window, horizontalThread, verticalThread):
                super().__init__()
                self.setParent(window)
                self.leftRightServoThread = horizontalThread
                self.upDownServoThread = verticalThread
                x = 0
                y = 0
       
        def mouseMoveEvent(self, event):
                x = round(180-(event.x() / 2))
                y = round((event.y() / 2) + 10)
                QToolTip.showText(QCursor.pos(), str(x) + "," + str(y))
                
                #Set thread
                self.leftRightServoThread.set_Y_POS(True, x)
                self.upDownServoThread.set_X_POS(True, y)
# --------------------------------------------------------------------------------------------------------------
# --------------------------------- Left Button Class ----------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------                        
class Left_Button(QPushButton):
    def __init__(self, window, text, thread):
        super(Left_Button, self).__init__()
        self.setText(text)
        self.setParent(window)
        self.servoThread = thread
           
    # Function call for the click event
    def On_Click(self):
        self.setIcon(QIcon(Left_Button_Pressed_Path))
        self.servoThread.set_leftButton(True)
# --------------------------------------------------------------------------------------------------------------
# --------------------------------- Right Button Class ---------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------                
class Right_Button(QPushButton):
    def __init__(self, window, text, thread):
        super(Right_Button, self).__init__()
        self.setText(text)
        self.setParent(window)
        self.servoThread = thread
        
    # Function call for the click event
    def On_Click(self):
        self.setIcon(QIcon(Right_Button_Pressed_Path))
        self.servoThread.set_rightButton(True)
# --------------------------------------------------------------------------------------------------------------
# --------------------------------- Up Button Class ------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------         
class Up_Button(QPushButton):
    def __init__(self, window, text, thread):
        super(Up_Button, self).__init__()
        self.setText(text)
        self.setParent(window)
        self.servoThread = thread

    # Function call for the click event
    def On_Click(self):
        self.setIcon(QIcon(Up_Button_Pressed_Path))
        self.servoThread.set_upButton(True)
# --------------------------------------------------------------------------------------------------------------
# --------------------------------- Down Button Class ----------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------         
class Down_Button(QPushButton):
    def __init__(self, window, text, thread):
        super(Down_Button, self).__init__()
        self.setText(text)
        self.setParent(window)
        self.servoThread = thread
        
    # Function call for the click event
    def On_Click(self):
        self.setIcon(QIcon(Down_Button_Pressed_Path))
        self.servoThread.set_downButton(True)
 


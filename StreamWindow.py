from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot, QObject
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLineEdit, QLabel
from PyQt5.QtGui import QPixmap, QIcon, QFont, QTextCursor, QPalette, QImage, QBrush, QImage
from time import sleep
import os


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
        print(input_video)
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
    

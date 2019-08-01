# import pyqt5 gui libraries
from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot, QObject
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLineEdit, QLabel, QSizePolicy
from PyQt5.QtGui import QPixmap, QIcon, QFont, QTextCursor, QPalette, QImage, QBrush, QImage

from time import sleep
import os
import numpy as np

# --------------------------------------------------------------------------------------------------------------
# ----------------------------------- Video Stream QLabel Class ------------------------------------------------
# --------------------------------------------------------------------------------------------------------------   
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
        qimage = QImage(input_video, input_video.shape[1], input_video.shape[0], input_video.shape[1] * 3, QImage.Format_RGB888).rgbSwapped()
        pixmap = QPixmap.fromImage(qimage)
        self.setPixmap(pixmap)
        
    def ImagetoGUI(self, input_pic):
        pixmap = QPixmap(input_pic)
        self.setPixmap(pixmap)
        
    def RecordtoGUI(self, input_rec):
        pixmap = QPixmap(input_rec)
        self.setPixmap(pixmap)  
             
    def TimeLapsetoGUI(self, input_tlapse):
        pixmap = QPixmap(input_tlapse)
        self.setPixmap(pixmap)       
    

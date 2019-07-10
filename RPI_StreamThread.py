from picamera import PiCamera, Color
from picamera.exc import PiCameraValueError, PiCameraRuntimeError
import time
from time import sleep
import datetime
import os
from PyQt5.QtGui import QImage
from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot
import ntpath

# File Structure
Main_path = os.getcwd() + "/"
Image_Path = Main_path + "Snapshots/"
                
class QRPIVideoStreamThread(QThread):
	Video_Stream_signal = pyqtSignal(str)
	Error_Signal = pyqtSignal(str) 
    
	def __init__(self, RPICamera):
		QThread.__init__(self)
		self.camera = RPICamera

		self.VideoStream_Ready = False
		self.exitProgram = False
        
    #Sets up the program to initiate video stream
	def Set_Video_Stream_Ready(self, stream_Rdy):
		self.VideoStream_Ready = stream_Rdy
        
    #Sets up the program to exit when the main window is shutting down
	def Set_Exit_Program(self, exiter):
		self.exitProgram = exiter,
        
	def run(self):
		self.setPriority(QThread.HighestPriority)

		while (1):
			
                        #Set Video Stream to GUI Qlabel
			if (self.VideoStream_Ready != False):
				try:
					# PiCam Stream configuration
					self.camera.annotate_foreground = Color('black')
					self.camera.annotate_text = ("Nico's RPI Cam\n" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
					self.camera.annotate_background = Color.from_rgb_bytes(152, 251, 152) 
				
					for i, filename in enumerate(self.camera.capture_continuous(Image_Path + 'Stream_Temp', format = 'jpeg', splitter_port= 2)):
						self.camera.annotate_text = ("Nico's RPI Cam\n" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

						#emit frame captured
						self.Video_Streaming(filename)

						if (self.VideoStream_Ready != True):
							break
							
				except PiCameraValueError:
					self.SendError("Stream Error.. Try Again!")	
							
				except PiCameraRuntimeError:
					self.SendError("Stream Error.. Try Again!")	
					self.VideoStream_Ready = True
			
			if(self.exitProgram == True):
				self.exitProgram = False
				break
            
			time.sleep(0.01)
            
        #Emits the estring to console log GUI
	def Video_Streaming(self,stream_str):
		self.Video_Stream_signal.emit(stream_str) 
   
	# Emits error message to console log
	def SendError(self, string):
			self.Error_Signal.emit(string)              


from picamera import PiCamera, Color
from picamera.exc import PiCameraValueError, PiCameraRuntimeError
from picamera.array import PiRGBArray
import numpy as np

import time
from time import sleep
import datetime
import os
from io import BytesIO
from PyQt5.QtGui import QImage
from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot

# File Structure
Main_path = os.getcwd() + "/"
Image_Path = Main_path + "Snapshots/"
                
class QRPIVideoStreamThread(QThread):
	Video_Stream_signal = pyqtSignal(np.ndarray)
	#~ Video_Stream_signal = pyqtSignal(str)
	Error_Signal = pyqtSignal(str) 
    
	def __init__(self, RPICamera, raw):
		QThread.__init__(self)
		self.camera = RPICamera
		self.raw = raw

		self.VideoStream_Ready = False
		self.exitProgram = False
		self.filename =  't'
        
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
				
					#~ self.camera.capture_sequence(self.filename, splitter_port= 2) 
					#~ for i, frame in enumerate(self.camera.capture_continuous(self.raw, format = 'bgr', splitter_port= 2)): 
					for frame in (self.camera.capture_continuous(self.raw, format = 'bgr', splitter_port= 2)): 

						# grab the raw NumPy array representing the image, then initialize the timestamp and occupied/unoccupied text
						image = frame.array
						
						#emit frame data captured
						#~ self.Video_Streaming(self.filename)
						self.Video_Streaming(image)

						# clear the stream in preparation for the next frame
						self.raw.truncate(0)
						
						if (self.VideoStream_Ready != True):
							break
							
				except PiCameraValueError as e:
					print(e)
					self.SendError("Stream Error.. Try Again!")	
							
				except PiCameraRuntimeError as e:
					print(e)
					self.SendError("Stream Error.. Try Again!")	
					self.VideoStream_Ready = True
			
			if(self.exitProgram == True):
				self.exitProgram = False
				break
            
			time.sleep(0.02)
            
        #Emits the estring to console log GUI
	def Video_Streaming(self,stream_str):
		self.Video_Stream_signal.emit(stream_str) 
   
	# Emits error message to console log
	def SendError(self, string):
			self.Error_Signal.emit(string)              


from picamera import PiCamera, Color
from picamera.exc import PiCameraValueError, PiCameraRuntimeError
from picamera.array import PiRGBArray
import numpy as np
import imutils
import cv2
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
                
# --------------------------------------------------------------------------------------------------------------
# ----------------------------------- VIdeo Stream Thread Class ------------------------------------------------
# --------------------------------------------------------------------------------------------------------------   
class QRPIVideoStreamThread(QThread):
	Video_Stream_signal = pyqtSignal(np.ndarray)
	Error_Signal = pyqtSignal(str) 
    
	def __init__(self, RPICamera, raw):
		QThread.__init__(self)
		self.camera = RPICamera
		self.raw = raw
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
					ts = datetime.datetime.now().strftime("%d %B %Y %I:%M:%S%p")
					self.camera.annotate_text = ("RPI Cam: " + ts)
					self.camera.annotate_background = Color.from_rgb_bytes(152, 251, 152) 
				
					# If motion detection is checked 
					self.motionDetection()
					
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
            
			time.sleep(1)
# ------------------------------------------------------------------			
# ------------Motion Detection Function ----------------------------
# ------------------------------------------------------------------			
	def motionDetection(self):
		avg = None

		for frame in (self.camera.capture_continuous(self.raw, format = 'bgr', splitter_port= 2)): 

						# PiCam Stream configuration
						self.camera.annotate_foreground = Color('black')
						ts = datetime.datetime.now().strftime("%d %B %Y %I:%M:%S%p")
						self.camera.annotate_text = ("RPI Cam: " + ts + "\n Motion {Not Detected}")
						self.camera.annotate_background = Color.from_rgb_bytes(152, 251, 152) 
					
						# grab the raw NumPy array representing the image
						image = frame.array
						
						# resize the frame, convert it to grayscale, and blur it
						#~ image = imutils.resize(image, width=500)
						gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
						gray = cv2.GaussianBlur(gray, (21, 21), 0)
 
						# if the average frame is None, initialize it
						if avg is None:
							#print("[INFO] starting background model...")
							avg = gray.copy().astype("float")
		
						# clear the stream in preparation for the next frame
						self.raw.truncate(0)
						
						# accumulate the weighted average between the current frame and
						# previous frames, then compute the difference between the current
						# frame and running average
						cv2.accumulateWeighted(gray, avg, 0.5)
						frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(avg))
						
						# threshold the delta image, dilate the thresholded image to fill
						# in holes, then find contours on thresholded image
						thresh = cv2.threshold(frameDelta, 5, 255, cv2.THRESH_BINARY)[1]
						thresh = cv2.dilate(thresh, None, iterations=2)
						cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
						cnts = imutils.grab_contours(cnts)
					 
						# loop over the contours
						for c in cnts:
							# if the contour is too small, ignore it
							if cv2.contourArea(c) < 5000:
								continue
					 
							# compute the bounding box for the contour, draw it on the frame,
							(x, y, w, h) = cv2.boundingRect(c)
							cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
							
							ts = datetime.datetime.now().strftime("%d %B %Y %I:%M:%S%p")
							self.camera.annotate_text = ("RPI Cam: " + ts + "\n Motion {Detected}")
							
							#Can add code later to record video/ pic/...etc

						#emit frame data captured
						self.Video_Streaming(image)
						
						if (self.VideoStream_Ready != True):
							break
# ------------------------------------------------------------------			
# ------------Face Recognition Function ----------------------------
# ------------------------------------------------------------------     
	def faceRecognition(self):
		pass      
		
# ------------------------------------------------------------------			
# ------------Emit Signals Functions -------------------------------
# ------------------------------------------------------------------  		
        #Emits the estring to console log GUI
	def Video_Streaming(self,stream_str):
		self.Video_Stream_signal.emit(stream_str) 
   
	# Emits error message to console log
	def SendError(self, string):
			self.Error_Signal.emit(string)              


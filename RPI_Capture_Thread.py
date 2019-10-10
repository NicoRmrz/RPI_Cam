from picamera import PiCamera, Color
from picamera.exc import PiCameraValueError
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

# --------------------------------------------------------------------------------------------------------------
# --------------------------------- Capture Image Thread Class -------------------------------------------------
# --------------------------------------------------------------------------------------------------------------   
class QRPICaptureThread(QThread):
	Snap_Captured_signal = pyqtSignal(str)
	Send_Image_signal = pyqtSignal(str)
	Status_Signal = pyqtSignal(int)
	Capture_Terminated_signal = pyqtSignal(int)
	Btn_Handler = pyqtSignal(str) 
	Error_Signal = pyqtSignal(str) 
	
	def __init__(self, RPICamera):
		QThread.__init__(self)

		self.camera = RPICamera
		self.exitProgram = False
		self.Snapshot_Ready = False
		self.Stop_Rec = False
		self.Record_Ready = False
		self.VideoStream_Ready = False
		self.TimeLapse_Ready = False
			
	#Sets up the program to exit when the main window is shutting down
	def Set_Exit_Program(self, exiter):
			self.exitProgram = exiter

	#Sets the program to initiate recording video
	def Set_Record_Ready(self, Rec_Rdy):
			self.Record_Ready = Rec_Rdy
			
	#Sets up the program to initiate camera snapshot
	def Set_Snapshot_Ready(self, Snap_Rdy):
			self.Snapshot_Ready = Snap_Rdy
			
	#Sets the program to initiate time lapse
	def Set_TimeLapse_Ready(self, TLpapse_Rdy):
			self.TimeLapse_Ready = TLpapse_Rdy

	#Sets the program to stop recording video  
	def Set_Stop(self, stp_rdy):
			self.Stop_Rec = stp_rdy
			
	#Function to get and emit recording status 
	def Get_Rec_Status(self):
			rec_status = self.camera.recording
			
			#Snap taken from recording
			if (rec_status != False or self.TimeLapse_Ready != False):
					self.Status_Signal.emit(1) 
				
			#Snap taken by itself
			else:
					self.Status_Signal.emit(0)
			
	#Function to reset video stream annotation text and background colors when stop button is pressed
	def reset_Stream(self):
			self.camera.annotate_foreground = Color('black')
			self.camera.annotate_text = ("Nico's RPI Cam\n" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
			self.camera.annotate_background = Color.from_rgb_bytes(152, 251, 152)                
		
	def run(self):
			self.setPriority(QThread.HighestPriority)

			while (1):
				
					#Set capture snapshot
					if (self.Snapshot_Ready != False and self.Record_Ready != True and self.Stop_Rec != True and self.TimeLapse_Ready != True):
															 
							try:								 
								# PiCam Stream Text
								self.camera.annotate_background = Color('blue')
								self.camera.annotate_foreground = Color('white')
								ts = datetime.datetime.now().strftime("%d %B %Y %I:%M:%S%p")
								self.camera.annotate_text = (ts)

								# Save image with timestamp
								currentTime = time.strftime('%Y-%m-%d__%H_%M_%S')
								Saved_Snap_Name = Image_Path + "Pup_Snap_" + currentTime + ".jpg"
								self.camera.capture(Saved_Snap_Name, splitter_port = 0)

								# emit image to GUI QLabel
								self.Display_Capture(Saved_Snap_Name)
								
								# emit saved file name
								curr_path, filename = ntpath.split(Saved_Snap_Name)
								self.SnapToGUI(filename)
								
								if (self.Stop_Rec != False):
												self.Procedure_Terminated("Procedure Stopped!")
												self.reset_Stream()
												
												#Exit loop
												self.Stop_Rec = False
															
							except PiCameraValueError:
								self.SendError("Something went wrong with the camera.. Try Again!")
								self.ButonResethandler("Capture")
							
							finally:
								#Exit loop
								self.Snapshot_Ready = False
				   
					if (self.Stop_Rec != False):
							self.reset_Stream()        
							self.Procedure_Terminated("Procedure Stopped!")   
							self.Record_Ready = False
							self.TimeLapse_Ready = False
							self.Snapshot_Ready = False
							
							#Exit loop
							self.Stop_Rec = False

					if(self.exitProgram == True):
							self.exitProgram = False
							break

					sleep(1)
					
	#Emits the string to console log GUI
	def SnapToGUI(self,snap_str):
			self.Snap_Captured_signal.emit(snap_str)   
			
	#Emits the image to GUI QLabel
	def Display_Capture(self, pic_str):
			self.Send_Image_signal.emit(pic_str)    
			
	#Emits video recording stopped
	def Procedure_Terminated(self, Name_Scheme):
			self.Capture_Terminated_signal.emit(Name_Scheme)                

	#Emits resets to gui pending button presses
	def ButonResethandler(self, ToGui):
			self.Btn_Handler.emit(ToGui)
			
	# Emits error message to console log
	def SendError(self, string):
			self.Error_Signal.emit(string)

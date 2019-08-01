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
Video_Path = Main_path + "Videos/"
TimeLapse_Path = Main_path + "Time_Lapse/"
WAIT_BETWEEN_CAPTURE = 5

# --------------------------------------------------------------------------------------------------------------
# --------------------------------- TimeLapse Thread Class -----------------------------------------------------
# --------------------------------------------------------------------------------------------------------------   
class QRPITimeLapseThread(QThread):

	Time_Lapse_Signal = pyqtSignal(str)
	Time_Lapse_imgName = pyqtSignal(str)
	Time_Lapse_String = pyqtSignal(str)
	CaptureWhileTimeLapse = pyqtSignal(str)
	Btn_Handler = pyqtSignal(str) 
	Error_Signal = pyqtSignal(str) 

	def __init__(self, RPICamera):
			QThread.__init__(self)
			self.camera = RPICamera 
			self.exitProgram = False
			self.Record_Ready = False
			self.Stop_Rec = False
			self.VideoStream_Ready = False
			self.TimeLapse_Ready = False
			self.Snapshot_Ready = False
			
	#Sets up the program to exit when the main window is shutting down
	def Set_Exit_Program(self, exiter):
			self.exitProgram = exiter

	#Sets the program to initiate recording video
	def Set_Record_Ready(self, Rec_Rdy):
			self.Record_Ready = Rec_Rdy
			
	#Sets the program to initiate time lapse
	def Set_TimeLapse_Ready(self, TLpapse_Rdy):
			self.TimeLapse_Ready = TLpapse_Rdy
			
	#Sets up the program to initiate camera snapshot
	def Set_Snapshot_Ready(self, Snap_Rdy):
		self.Snapshot_Ready = Snap_Rdy

	#Sets the program to stop recording video  
	def Set_Stop(self, stp_rdy):
			self.Stop_Rec = stp_rdy
			
	 #Create video of timelape after stop button is pressed
	def SaveTimelapse(self):
			os.chdir(TimeLapse_Path)
			currentTime = time.strftime('%Y-%m-%d__%H_%M_%S')
			ConvertVideo =  "avconv -r 10 -i img%03d.jpg -r 10 -vcodec libx264 -vf scale=1280:720 " + "timelapse_" + currentTime + ".mp4"
			os.system(ConvertVideo)
			self.TimeLapse_Finsihed("timelapse_" + currentTime + ".mp4")
			
	#Remove all image files from timelapse folder after video is created.
	def cleanUp(self):
			os.chdir(TimeLapse_Path)
			for filename in os.listdir():
				if filename.startswith('img'):
					 os.unlink(filename)
					 
	#~ #Function to get and emit recording status 
	#~ def Get_Rec_Status(self):
			#~ rec_status = self.camera.recording
			
			#~ #Snap taken from recording
			#~ if (rec_status != False or self.TimeLapse_Ready != False):
					#~ self.Status_Signal.emit(1) 
				
			#~ #Snap taken by itself
			#~ else:
					#~ self.Status_Signal.emit(0)
			
	#Function to reset video stream annotation text and background colors when stop button is pressed
	def reset_Stream(self):
			self.camera.annotate_foreground = Color('black')
			self.camera.annotate_text = ("Nico's RPI Cam\n" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
			self.camera.annotate_background = Color.from_rgb_bytes(152, 251, 152)                
		
	def run(self):
			self.setPriority(QThread.HighestPriority)

			while (1):
				
					#Set Time Lapse
					if (self.TimeLapse_Ready != False and self.Snapshot_Ready != True and self.Record_Ready != True and self.Stop_Rec != True):
							try:
								self.camera.annotate_background = Color('orange')
								self.camera.annotate_foreground = Color('black')
								self.camera.annotate_text = ("Timelapse... \n" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
						
								for filename in self.camera.capture_continuous(TimeLapse_Path + 'img{counter:03d}.jpg', use_video_port=True):
										self.camera.annotate_background = Color('orange')
										self.camera.annotate_foreground = Color('black')
										self.camera.annotate_text = ("Timelapse... \n" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
														
										# emit current time lapse image to GUI QLabel		
										self.TimeLapse_to_GUI(filename)
													
										# emit saved file name
										curr_path, filename = ntpath.split(filename)									
										self.sendImgName(filename)
																			
										sleep(WAIT_BETWEEN_CAPTURE)  # wait in seconds between iamges
										
										#If camera is pressed during timelapse
										if (self.Snapshot_Ready != False and self.Stop_Rec != True):
												try:
													# Save image with timestamp
													currentTime = time.strftime('%Y-%m-%d__%H_%M_%S')
													Saved_Snap_Name = Image_Path + "Pup_TimeLapse_Snap_" + currentTime + ".jpg"
													self.camera.capture(Saved_Snap_Name, splitter_port = 0)

													# emit saved file name
													curr_path, filename = ntpath.split(Saved_Snap_Name)
													self.captureWhileTimeLapse(filename)
													
												except PiCameraValueError:
													self.SendError("Something went wrong with the camera.. Try Again!")	
													self.ButonResethandler("Capture")
													
												finally:
													self.ButonResethandler("Capture")
													#Exit loop
													self.Snapshot_Ready = False
		
										if (self.Stop_Rec != False):							
												self.reset_Stream()
												self.SaveTimelapse()
												self.cleanUp()
												
												# Exit loop
												self.TimeLapse_Ready = False 
												
												self.Stop_Rec = False
												break
												
							except PiCameraValueError:
								self.SendError("Something went wrong with the camera.. Try Again!")
								self.ButonResethandler("TimeLapse")
																												
					if (self.Stop_Rec != False):
							self.reset_Stream()
							self.Record_Ready = False
							self.TimeLapse_Ready = False
							self.Snapshot_Ready = False
							self.ButonResethandler("TimeLapse")
							
							#Exit loop
							self.Stop_Rec = False

					if(self.exitProgram == True):
							self.exitProgram = False
							break

					sleep(1)
						
	#Emits Time Lapse Image to GUI QLabel
	def TimeLapse_to_GUI(self, tlapse_str):
			self.Time_Lapse_Signal.emit(tlapse_str)
                
	 #Emits Time Lapse finished
	def TimeLapse_Finsihed(self, tlapse_str):
			self.Time_Lapse_String.emit(tlapse_str)     
			
	#Emits Time Lapse Image name to text edit window
	def sendImgName(self, tlapse_str):
			self.Time_Lapse_imgName.emit(tlapse_str)
			
	#Emits Time Lapse Image name when capture while timelapse
	def captureWhileTimeLapse(self, tlapse_str):
			self.CaptureWhileTimeLapse.emit(tlapse_str)

	#Emits resets to gui pending button presses
	def ButonResethandler(self, ToGui):
			self.Btn_Handler.emit(ToGui)
			
	# Emits error message to console log
	def SendError(self, string):
			self.Error_Signal.emit(string)

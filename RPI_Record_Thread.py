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

        
class QRPIRecordVideoThread(QThread):
	Recording_Completed_signal = pyqtSignal(str)
	Recording_Terminated_signal = pyqtSignal(str)
	Rec_GUI_signal = pyqtSignal(str)
	Status_Signal = pyqtSignal(int)
	Btn_Handler = pyqtSignal(str)    
	Error_Signal = pyqtSignal(str) 
	Snap_while_recording_signal = pyqtSignal(str)
	Stop_PBar = pyqtSignal(str)

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
	def Set_Record_Ready(self, Rec_Rdy, Rec_Time):
		self.Record_Ready = Rec_Rdy
		self.Rec_Time = Rec_Time
			
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
				
					#Set record video
					if (self.Record_Ready != False and self.Stop_Rec != True and self.Snapshot_Ready != True and self.TimeLapse_Ready != True):
							try:	
								# Start recording video
								currentTime = time.strftime('%Y-%m-%d__%H_%M_%S')
								Vid_Name_Scheme = Video_Path +"Video_" + currentTime + ".h264"
								self.camera.start_recording(Vid_Name_Scheme, splitter_port=1)
								start = datetime.datetime.now()
								
								self.camera.annotate_background = Color('pink')
								self.camera.annotate_foreground = Color('black')
								self.camera.annotate_text = ("Recording...\n" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
										
								#Countdown loop for recording with input time.
								while ((datetime.datetime.now() - start).seconds < int(self.Rec_Time) and self.Stop_Rec != True):
										
										self.camera.annotate_background = Color('pink')
										self.camera.annotate_foreground = Color('black')
										self.camera.annotate_text = ("Recording... \n" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
										
										self.camera.wait_recording(0.2, splitter_port=1)
										
										# Save current frame to emit to GUI
										currentTime = time.strftime('%Y-%m-%d__%H_%M_%S')
										Temp_Snap_Name = Image_Path + "Vid_Temp" + ".jpg"
										self.camera.capture(Temp_Snap_Name, use_video_port=True)
										
										# emit recording to GUI QLabel
										self.Recording_to_GUI(Temp_Snap_Name)
										
										# Get status if video is recording
										rec_status = self.camera.recording
																		
										# If camera is pressed during video
										if (self.Snapshot_Ready != False and rec_status != False and self.Stop_Rec != True):
												try:
													# Save image with timestamp
													currentTime = time.strftime('%Y-%m-%d__%H_%M_%S')
													Saved_Snap_Name = Image_Path + "Pup_Rec_Snap_" + currentTime + ".jpg"
													self.camera.capture(Saved_Snap_Name, splitter_port=0)

													# emit saved file name
													curr_path, filename = ntpath.split(Saved_Snap_Name)
													self.SnapToGUI(filename)
																									
												except PiCameraValueError:
													self.SendError("Something went wrong with the camera.. Try Again!")
													self.ButonResethandler("Capture")
													print(e)
												
												finally:	
													self.ButonResethandler("Capture")
													# Exit loop
													self.Snapshot_Ready = False
								
										# If Stop button in pressed
										if (self.Stop_Rec != False):
												self.reset_Stream()
												self.Recording_Terminated("Procedure Stopped!")
												
												#Exit loop
												self.Rec_Time = 0
												self.Record_Ready = False
												self.Stop_Rec = False
										
										# Reset timelapse button if pressed while recording
										if (self.TimeLapse_Ready != False):
												self.ButonResethandler("TimeLapse")
												self.TimeLapse_Ready = False
		   
								
																
							except PiCameraValueError:
								self.SendError("Something went wrong with the camera.. Try Again!")
								self.ButonResethandler("Record")
								self.Stop_PBar.emit("True")
								self.ButonResethandler("Stream")
							
							finally:	
								self.camera.stop_recording(splitter_port=1)  
																
								# emit saved file name
								curr_path, filename = ntpath.split(Vid_Name_Scheme)
								self.Recording_Finished(filename)
								
								# Exit loop
								self.Record_Ready = False
						
					if (self.Stop_Rec != False):		
							self.reset_Stream()
							self.Record_Ready = False
							self.TimeLapse_Ready = False
							self.Snapshot_Ready = False						
							self.Recording_Terminated("Procedure Stopped!")
							
							#Exit loop
							self.Stop_Rec = False

					if(self.exitProgram == True):
							self.exitProgram = False
							break

					sleep(1)		  

	#Emits video recording finished
	def Recording_Finished(self, Name_Scheme):
			self.Recording_Completed_signal.emit(Name_Scheme)      

	#Emits video recording stopped
	def Recording_Terminated(self, Name_Scheme):
			self.Recording_Terminated_signal.emit(Name_Scheme) 
			
	#Emits recording video to GUI QLabel
	def Recording_to_GUI(self, rec_str):
			self.Rec_GUI_signal.emit(rec_str)
			
	#Emits the snapshot taken while recording name to console log
	def SnapToGUI(self,snap_str):
			self.Snap_while_recording_signal.emit(snap_str) 
			
	#Emits resets to gui pending button presses
	def ButonResethandler(self, ToGui):
			self.Btn_Handler.emit(ToGui)

	# Emits error message to console log
	def SendError(self, string):
			self.Error_Signal.emit(string)
                
class QPBarThread(QThread):
	Update_prog_bar_signal = pyqtSignal(int)
	Btn_Handler = pyqtSignal(str)    

	def __init__(self, recordThre):
		QThread.__init__(self)
		self.set_UpdatePBar = False
		self.exitProgram = False
		self.stopPbar = False
		self.stopFromThread = False
		self.recordThread = recordThre
		
		# Connect signal from record thread to stop progress bar
		self.recordThread.Stop_PBar.connect(self.stop_PBar)
        
        #Sets up the program to exit when the main window is shutting down
	def Set_Exit_Program(self, exiter):
		self.exitProgram = exiter
		
	# Set function to increment progress bar
	def set_increment_ProgressBar(self, totalTime, set_update):
		self.TotalTime = int(totalTime)
		self.set_UpdatePBar = set_update
		
	# set funciton to stop progress bar from stop button
	def Set_Stop_Bar(self, update):
		self.stopPbar = update
		
	# function to stop progress bar from error in record thread
	def stop_PBar(self, stopStr):
		if stopStr == "True":
			self.stopFromThread = True
		else:
			self.stopFromThread = False	
		self.ButonResethandler("ProgressBar")

	def run(self):
		self.setPriority(QThread.HighestPriority)

		while (1):
			
			if (self.set_UpdatePBar != False and self.stopPbar != True and self.stopFromThread != True):
				print("Recording for " + str(self.TotalTime) + "s")
				progress_step = 0
				progress_inc = 100 / self.TotalTime
				count = 0
				
				while (count < self.TotalTime and self.stopPbar != True and self.stopFromThread != True):
					count += 1 
					     
					# Increments Progress Bar
					progress_step += progress_inc
					self.Update_Prog_Bar(progress_step)
					
					time.sleep(1) #increments by the second
					print(count)
			
				# To Exit loop
				self.set_UpdatePBar = False
			
			# To reset stopPBar
			if (self.stopPbar != False):
				
				#Exit loop
				self.stopPbar = False                              
                        
			# To reset stopFromThread        
			if (self.stopFromThread != False):
				
				#Exit loop
				self.stopFromThread = False                              
				
			if(self.exitProgram == True):
				self.exitProgram = False
				break

			time.sleep(1)
            
	#Emits update to progress bar
	def Update_Prog_Bar(self,updt_prgBar):
		self.Update_prog_bar_signal.emit(updt_prgBar)  
		
	#Emits resets to gui pending button presses
	def ButonResethandler(self, ToGui):
		self.Btn_Handler.emit(ToGui)

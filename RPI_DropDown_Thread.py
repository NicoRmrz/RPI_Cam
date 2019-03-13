from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot
from picamera.exc import PiCameraValueError, PiCameraMMALError
from time import sleep


class QDropDownThread(QThread):

	imgEffect_Sig = pyqtSignal(str)
	exposureMode_Sig = pyqtSignal(str)
	resFrmrt_Sig = pyqtSignal(str, str)
	Error_Signal = pyqtSignal(str) 
	Reset_Signal = pyqtSignal(str) 

	def __init__(self, RPICamera):
		QThread.__init__(self)
		self.camera = RPICamera
		self.exitProgram = False
		self.imgEffectReady = False
		self.exposureReady = False
		self.resFrmReady = False
		
	# Set for the drop down combo box
	def set_imgEffectReady(self, string, selection):
		self.imgEffectReady = string
		self.imeEffectSel = selection
	 
	# Set for the drop down combo box
	def set_exposureModeReady(self, string, selection):
		self.exposureReady = string
		self.exposureSel = selection
	 
	# Set for the drop down combo box
	def set_resolutionFramerateReady(self, string, selection):
		self.resFrmReady = string
		self.resFrmSel = selection

	#Sets up the program to exit when the main window is shutting down
	def Set_Exit_Program(self, exiter):
		self.exitProgram = exiter

    #This function is started by .start() and runs the main portion of the code
	def run(self):

		while(1):
          
			#set for change in image effect
			if (self.imgEffectReady != False):
				self.camera.image_effect = self.imeEffectSel 
				self.changeImageEffect(self.imeEffectSel)
				sleep(0.3)

				# Exit Loop
				self.imgEffectReady = False
          
			#set for change in exposure mode
			if (self.exposureReady != False):
				self.camera.exposure_mode = self.exposureSel 
				self.changeExposureMode(self.exposureSel)
				sleep(0.3)

				# Exit Loop
				self.exposureReady = False
          
			#set for change in resolution and framerate mode
			if (self.resFrmReady != False):
				if self.resFrmSel =="1640x1232 @ 30 fps":
					try:
						self.camera.resolution = (1640, 1232)
						self.camera.framerate = 30 
						
						#To emit done with selection
						self.changeResolutionFramerate("1640x1232", "30")
						
					except PiCameraMMALError as e:
						self.SendError("Something went wrong.. MMALError")
						self.resetAllStreams("Reset")
						print(e)			
								
					finally:
						# Exit Loop
						self.resFrmReady = False
					
				elif  self.resFrmSel == "1640x922 @ 30 fps":
					try:
						self.camera.resolution = (1640, 922)
						self.camera.framerate = 30 
						
						#To emit done with selection
						self.changeResolutionFramerate("1640x922", "30")
						
					except PiCameraMMALError as e:
						self.SendError("Something went wrong.. MMALError")
						self.resetAllStreams("Reset")
						print(e)			
								
					finally:
						# Exit Loop
						self.resFrmReady = False
					
				elif  self.resFrmSel == "1280x720 @ 40 fps":
					try:
						self.camera.resolution = (1280, 720)
						self.camera.framerate = 40 
						
						#To emit done with selection
						self.changeResolutionFramerate("1280x720", "40")
						
					except PiCameraMMALError as e:
						self.SendError("Something went wrong.. MMALError")
						self.resetAllStreams("Reset")
						print(e)			
								
					finally:
						# Exit Loop
						self.resFrmReady = False
					
				elif  self.resFrmSel == "640x480 @ 60 fps":
					try:
						self.camera.resolution = (640, 480)
						self.camera.framerate = 60 
						
						#To emit done with selection
						self.changeResolutionFramerate("640x480", "60")
						
					except PiCameraMMALError as e:
						self.SendError("Something went wrong.. MMALError")
						self.resetAllStreams("Reset")
						print(e)			
								
					finally:
						# Exit Loop
						self.resFrmReady = False				
				
				sleep(0.3)
				# Exit Loop
				self.resFrmReady = False
						  
			if(self.exitProgram == True):
				self.exitProgram = False
				break

			sleep(1)

	# Function to emit done after selecting the Image Effect
	def changeImageEffect(self, value):
		self.imgEffect_Sig.emit(value)

	# Function to emit done after selecting the exposure mode
	def changeExposureMode(self, value):
		self.exposureMode_Sig.emit(value)

	# Function to emit done after selecting the resolution and framerate
	def changeResolutionFramerate(self, resolution, framerate):
		self.resFrmrt_Sig.emit(resolution, framerate)
			
	# Emits error message to console log
	def SendError(self, string):
		self.Error_Signal.emit(string)
   
	# Emits reset to continue streams
	def resetAllStreams(self, string):
		self.Reset_Signal.emit(string)
   
  

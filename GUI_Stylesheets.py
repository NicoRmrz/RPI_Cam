from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot, QObject, QSize

class GUI_Stylesheets(QObject):
	
	 # Initializes the necessary objects into the slider class for control
	def __init__(self):
		super(GUI_Stylesheets, self).__init__()
		
		self.mainWindow = 	("background-color: #95c8d8") 
		
		self.mainTitle =	("font: bold 35px Verdana; "
							"color: white; "
							"background-color: rgba(18,151,147,0)"
							)
		
		self.tabs = 	("QTabWidget::pane {border-top: 1px solid white;} "
						"QTabWidget::tab-bar {left: 5px;} "
						"QTabBar::tab {background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, "
							"stop: 0 #E1E1E1, "
							"stop: 0.4 #DDDDDD, "
							"stop: 0.5 #D8D8D8, "
							"stop: 1.0 #D3D3D3); "
							"border: 2px solid #C4C4C3; "
							"border-bottom-color: #C2C7CB; "
							"border-top-left-radius: 4px; "
							"border-top-right-radius: 4px; "
							"min-width: 0px; "
							"padding: 2px;} "
						"QTabBar::tab:selected, "
						"QTabBar::tab:hover {background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, "
							"stop: 0 #fafafa, "
							"stop: 0.4 #f4f4f4, "
							"stop: 0.5 #e7e7e7, "
							"stop: 1.0 #fafafa);} "
						"QTabBar::tab:selected {border-color: #9B9B9B; "
							"border-bottom-color: #C2C7CB;} "
						"QTabBar::tab:!selected {margin-top: 2px;} "
						"QTabBar::tab:selected {margin-left: -4px; "
							"margin-right: -4px;} "
						"QTabBar::tab:first:selected {margin-left: 0;} "
						"QTabBar::tab:last:selected {margin-right: 0;} "
						"QTabBar::tab:only-one {margin: 0;}"
						)
		
		self.statusBar = ("QStatusBar { background: #95c8d8; "
										"color:white;} "

							"QStatusBar::item {border: 1px solid #95c8d8; "
								"border-radius: 3px; }"
								
							)
							
		self.statusBar_XY	= (	"QLabel {border: none; "
								"background-color: qlineargradient(spread:pad x1:0.45, y1:0.3695, x2:0.427, y2:0, "
								"stop:0 rgba(242, 242, 242, 0), "
								"stop:1 rgba(242,242,242, 0)); "						
								"font: 20 px; "
								"font-weight: bold; "
								"color: black; }"			
							)			
							
		self.statusBar_widgets	= (	"QLabel {border: none; "
								"background-color: qlineargradient(spread:pad x1:0.45, y1:0.3695, x2:0.427, y2:0, "
								"stop:0 rgba(242, 242, 242, 0), "
								"stop:1 rgba(242,242,242, 0)); "						
								"font: 20 px; "
								"font-weight: lighter; "
								"color: black; }"			
							)			
		
		self.videoStream = 	("background-color: qlineargradient(spread:pad x1:0.45, y1:0.3695, x2:0.427, y2:0, "
								"stop:0 rgba(242, 242, 242, 100), "
								"stop:1 rgba(242,242,242,100))"
							)
		
		self.consoleLog	=	("font: 12px Verdana; "
							"background-color: qlineargradient(spread:pad x1:0.45, y1:0.3695, x2:0.427, y2:0, "
								"stop:0 rgba(242, 242, 242, 240), "
								"stop:1 rgba(255,255,255,255))"
							)
		
		self.progressBar = 	("QProgressBar::chunk {background-color: #CD96CD;} "
							"background-color: qlineargradient(spread:pad x1:0.45, y1:0.3695, x2:0.427, y2:0, "
								"stop:0 rgba(242, 242, 242, 240), "
								"stop:1 rgba(255,255,255,255))"
							)
							
		self.startButton = 	("font: bold 12px Verdana; "
							"background-color: qlineargradient(spread:pad x1:0.45, y1:0.3695, x2:0.427, y2:0, "
								"stop:0 rgba(242, 242, 242, 0), "
								"stop:1 rgba(255,255,255,0)); "
								"border-style: outset; "
								"border-radius: 4px"
							)
							
		self.recordButton = ("font: bold 12px Verdana; "
							"background-color: qlineargradient(spread:pad x1:0.45, y1:0.3695, x2:0.427, y2:0, "
								"stop:0 rgba(250, 218, 94, 0), "
								"stop:1 rgba(255,255,255,0)); "
								"border-style: outset; "
								"border-radius: 4px; "
							)
        
		self.timelapseButton = 	("font: bold 12px Verdana; "
								"background-color: qlineargradient(spread:pad x1:0.45, y1:0.3695, x2:0.427, y2:0, "
									"stop:0 rgba(250, 218, 94, 0), "
									"stop:1 rgba(255,255,255,0)); "
									"border-style: outset; "
									"border-radius: 4px"
								)

		self.stopButton	=	("font: bold 12px Verdana; "
							"color: white; "
							"background-color: qlineargradient(spread:pad x1:0.45, y1:0.3695, x2:0.427, y2:0, "
								"stop:0 rgba(250, 41, 57, 0), "
								"stop:1 rgba(255,255,255,0)); "
								"border-style: outset; "
								"border-radius: 4px"
							)

		self.sliderLabel =	("font: bold 14px Verdana; "
							"color: white; "
							"background-color: rgba(18,151,147,0)"
							)
		
		self.sliderNumber =	("font: bold 16px Verdana; "
							"color: white; "
							"background-color: rgba(0,0,0,0)"
							)

		self.brightnessSlider =	("QSlider::groove:horizontal {border: 1px solid #bbb; "
									"background: white; "
									"height: 8px; "
									"border-radius: 4px} "
        
								"QSlider::handle:horizontal {background: qlineargradient(x1: 0, y1: 0,  x2: 0, y2: 1, "
									"stop: 0 #B5D3e7, "
									"stop: 1 #fff); "
									"border: 1px solid #777; "
									"width: 15px; "
									"height: 15px; "
									"margin-top: -4px; "
									"margin-bottom: -4px; "
									"border-radius: 9px; } "
								
								"QSlider::sub-page:horizontal {background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, "
									"stop: 0 #Fd6A06, "
									"stop: 1 #Caccce); "
									"border: 1px solid #777; "
									"height: 10px; "
									"border-radius: 4px;}"
								
								"QSlider::add-page:horizontal {background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, "
									"stop: 0 #D8CaCa, "
									"stop: 1 #fff); "
									"background: qlineargradient(x1: 0, y1: 0.2, x2: 1, y2: 1, "
									"stop: 0 #fff, "
									"stop: 1 #D8CaCa); "
									"border: 1px solid #777; "
									"height: 10px; "
									"border-radius: 4px;} "
								)

		self.contrastSlider =	("QSlider::groove:horizontal {border: 1px solid #bbb; "
									"background: white; "
									"height: 8px; "
									"border-radius: 4px} "
        
								"QSlider::handle:horizontal {background: qlineargradient(x1: 0, y1: 0,  x2: 0, y2: 1, "
									"stop: 0 #B5D3e7, "
									"stop: 1 #fff); "
									"border: 1px solid #777; "
									"width: 15px; "
									"height: 15px; "
									"margin-top: -4px; "
									"margin-bottom: -4px; "
									"border-radius: 9px; }  "
							
								"QSlider::sub-page:horizontal {background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, "
									"stop: 0 #50c878, "
									"stop: 1 #Caccce); "
									"border: 1px solid #777; "
									"height: 10px; "
									"border-radius: 4px;}"
								
								"QSlider::add-page:horizontal {background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, "
									"stop: 0 #D8CaCa, "
									"stop: 1 #fff); "
								"background: qlineargradient(x1: 0, y1: 0.2, x2: 1, y2: 1, "
									"stop: 0 #fff, "
									"stop: 1 #D8CaCa); "
									"border: 1px solid #777; "
									"height: 10px; "
									"border-radius: 4px;} "
								)

		self.sharpnessSlider =	("QSlider::groove:horizontal {border: 1px solid #bbb; "
									"background: white; "
									"height: 8px; "
									"border-radius: 4px} "
        
								"QSlider::handle:horizontal {background: qlineargradient(x1: 0, y1: 0,  x2: 0, y2: 1, "
									"stop: 0 #B5D3e7, "
									"stop: 1 #fff); "
									"border: 1px solid #777; "
									"width: 15px; "
									"height: 15px; "
									"margin-top: -4px; "
									"margin-bottom: -4px; "
									"border-radius: 9px; }  "
								
								"QSlider::sub-page:horizontal {background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, "
									"stop: 0 #0080ff, "
									"stop: 1 #Caccce); "
									"border: 1px solid #777; "
									"height: 10px; "
									"border-radius: 4px;}"
								
								"QSlider::add-page:horizontal {background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, "
									"stop: 0 #D8CaCa, "
									"stop: 1 #fff); "
								"background: qlineargradient(x1: 0, y1: 0.2, x2: 1, y2: 1, "
									"stop: 0 #fff, "
									"stop: 1 #D8CaCa); "
									"border: 1px solid #777; "
									"height: 10px; "
									"border-radius: 4px;} "
								)
		
		self.saturationSlider =	("QSlider::groove:horizontal {border: 1px solid #bbb; "
									"background: white; "
									"height: 8px; "
									"border-radius: 4px} "

								"QSlider::handle:horizontal {background: qlineargradient(x1: 0, y1: 0,  x2: 0, y2: 1, "
									"stop: 0 #B5D3e7, "
									"stop: 1 #fff); "
									"border: 1px solid #777; "
									"width: 15px; "
									"height: 15px; "
									"margin-top: -4px; "
									"margin-bottom: -4px; "
									"border-radius: 9px; }  "

								"QSlider::sub-page:horizontal {background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, "
									"stop: 0 #9a6da5, "
									"stop: 1 #Caccce); "
									"border: 1px solid #777; "
									"height: 10px; "
									"border-radius: 4px;}"

								"QSlider::add-page:horizontal {background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, "
									"stop: 0 #D8CaCa, "
									"stop: 1 #fff); "
								"background: qlineargradient(x1: 0, y1: 0.2, x2: 1, y2: 1, "
									"stop: 0 #fff, "
									"stop: 1 #D8CaCa); "
									"border: 1px solid #777; "
									"height: 10px; "
									"border-radius: 4px;} "
								)
		
		self.verticalSlider =	("QSlider::groove:vertical {border: 1px solid #bbb; "
									"background: white; "
									"width: 8px; "
									"border-radius: 4px} "

								"QSlider::handle:vertical {background: qlineargradient(x1: 0, y1: 0,  x2: 0, y2: 1, "
									"stop: 0 #B5D3e7, "
									"stop: 1 #fff); "
									"border: 1px solid #777; "
									"width: 15px; "
									"height: 15px; "
									"margin-left: -4px; "
									"margin-right: -4px; "
									"border-radius: 9px; }  "

								"QSlider::sub-page:vertical {background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, "
									"stop: 0 #9a6da5, "
									"stop: 1 #Caccce); "
									"border: 1px solid #777; "
									"height: 10px; "
									"border-radius: 4px;}"

								"QSlider::add-page:vertical {background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, "
									"stop: 0 #D8CaCa, "
									"stop: 1 #fff); "
								"background: qlineargradient(x1: 0, y1: 0.2, x2: 1, y2: 1, "
									"stop: 0 #fff, "
									"stop: 1 #D8CaCa); "
									"border: 1px solid #777; "
									"height: 10px; "
									"border-radius: 4px;} "
								)
		
		self.annotationSlider =	("QSlider::groove:horizontal {border: 1px solid #bbb; "
									"background: white; "
									"height: 8px; "
									"border-radius: 4px} "
        
								"QSlider::handle:horizontal {background: qlineargradient(x1: 0, y1: 0,  x2: 0, y2: 1, "
									"stop: 0 #B5D3e7, "
									"stop: 1 #fff); "
									"border: 1px solid #777; "
									"width: 15px; "
									"height: 15px; "
									"margin-top: -4px; "
									"margin-bottom: -4px; "
									"border-radius: 9px; }  "

								"QSlider::sub-page:horizontal {background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, "
									"stop: 0 #FFFF88, "
									"stop: 1 #Caccce); "
									"border: 1px solid #777; "
									"height: 10px; "
									"border-radius: 4px;}"

								"QSlider::add-page:horizontal {background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, "
									"stop: 0 #D8CaCa, "
									"stop: 1 #fff); "
									"background: qlineargradient(x1: 0, y1: 0.2, x2: 1, y2: 1, "
									"stop: 0 #fff, "
									"stop: 1 #D8CaCa); "
									"border: 1px solid #777; "
									"height: 10px; "
									"border-radius: 4px;} "
								)  
		
		self.imageEffect =	("QComboBox {border: 1px solid gray; "
								"border-radius: 3px; "
								"padding: 1px 18px 1px 3px; "
								"min-width: 6em; } "  
							    
							"QComboBox:editable {background: white;} "
							
							"QComboBox:!editable, "
							"QComboBox::drop-down:editable {font: 15px; "
								"color: black; "
								"background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, "
								"stop: 0 #83ff78, "
								"stop: 0.25 #9aff91, " 
								"stop: 0.5 #b2ffab, "
								"stop: 0.75 #c9ffc4, "
								"stop: 1.0 #e0ffde);} "
							
							"QComboBox:hover {background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, "
								"stop: 0 #ffe476, "
								"stop: 0.25 #fffb9f, " 
								"stop: 0.5 #fff6c1, "
								"stop: 0.75 #fdffd8, "
								"stop: 1.0 #ffffff);} "
							
							"QComboBox:on {padding-top: 3px; "
								"padding-left: 4px; "
								"color: white; "
								"background: yellow;} "
						   
							"QComboBox::drop-down {subcontrol-origin: padding; "
								"subcontrol-position: top right; "
								"width: 20px; "
								"background: lightgrey; "
								"border-left-width: 1px; "
								"border-left-color: darkgray; "
								"border-left-style: solid; " 
								"border-top-right-radius: 3px; " 
								"border-bottom-right-radius: 3px;} "
								
							"QComboBox::down-arrow {image: url(/home/pi/Desktop/RPI_Cam/Icon_Image/arrow.png); "
								"height:15px; "
								"width:25px;} "
							"QComboBox::down-arrow:on {top: 1px; "
								"left: 1px;} "
								
							"QComboBox QAbstractItemView {border: 2px solid darkgray; "
								"selection-background-color: lightgrey;}"
							)
		
		self.exposureMode =	("QComboBox {border: 1px solid gray; "
								"border-radius: 3px; "
								"padding: 1px 18px 1px 3px; "
								"min-width: 6em; } "  
							    
							"QComboBox:editable {background: white;} "
							
							"QComboBox:!editable, "
							"QComboBox::drop-down:editable {font: 15px; "
								"color: black; "
								"background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, "
								"stop: 0 #ffaf88, "
								"stop: 0.25 #ffb997, " 
								"stop: 0.5 #ffc3a6, "
								"stop: 0.75 #ffcdb5, "
								"stop: 1.0 #ffd7c3);} "
							
							"QComboBox:hover {background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, "
								"stop: 0 #ffe476, "
								"stop: 0.25 #fffb9f, " 
								"stop: 0.5 #fff6c1, "
								"stop: 0.75 #fdffd8, "
								"stop: 1.0 #ffffff);} "
							
							"QComboBox:on {padding-top: 3px; "
								"padding-left: 4px; "
								"color: white; "
								"background: yellow;} "
						   
							"QComboBox::drop-down {subcontrol-origin: padding; "
								"subcontrol-position: top right; "
								"width: 20px; "
								"background: lightgrey; "
								"border-left-width: 1px; "
								"border-left-color: darkgray; "
								"border-left-style: solid; " 
								"border-top-right-radius: 3px; " 
								"border-bottom-right-radius: 3px;} "
								
							"QComboBox::down-arrow {image: url(/home/pi/Desktop/RPI_Cam/Icon_Image/arrow.png); "
								"height:15px; "
								"width:25px;} "
							"QComboBox::down-arrow:on {top: 1px; "
								"left: 1px;} "
								
							"QComboBox QAbstractItemView {border: 2px solid darkgray; "
								"selection-background-color: lightgrey;}"
							)
		
		self.resolutionFramerate =	("QComboBox {border: 1px solid gray; "
								"border-radius: 3px; "
								"padding: 1px 18px 1px 3px; "
								"min-width: 6em; } "  
							    
							"QComboBox:editable {background: white;} "
							
							"QComboBox:!editable, "
							"QComboBox::drop-down:editable {font: 15px; "
								"color: black; "
								"background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, "
								"stop: 0 #bca3fd, "
								"stop: 0.25 #c4affd, " 
								"stop: 0.5 #cdbafd, "
								"stop: 0.75 #d5c6fe, "
								"stop: 1.0 #ddd1fe);} "
							
							"QComboBox:hover {background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, "
								"stop: 0 #ffe476, "
								"stop: 0.25 #fffb9f, " 
								"stop: 0.5 #fff6c1, "
								"stop: 0.75 #fdffd8, "
								"stop: 1.0 #ffffff);} "
							
							"QComboBox:on {padding-top: 3px; "
								"padding-left: 4px; "
								"color: white; "
								"background: yellow;} "
						   
							"QComboBox::drop-down {subcontrol-origin: padding; "
								"subcontrol-position: top right; "
								"width: 20px; "
								"background: lightgrey; "
								"border-left-width: 1px; "
								"border-left-color: darkgray; "
								"border-left-style: solid; " 
								"border-top-right-radius: 3px; " 
								"border-bottom-right-radius: 3px;} "
								
							"QComboBox::down-arrow {image: url(/home/pi/Desktop/RPI_Cam/Icon_Image/arrow.png); "
								"height:15px; "
								"width:25px;} "
							"QComboBox::down-arrow:on {top: 1px; "
								"left: 1px;} "
								
							"QComboBox QAbstractItemView {border: 2px solid darkgray; "
								"selection-background-color: lightgrey;}"
							)

		self.mouseTrackPad = ("background-color: pink")

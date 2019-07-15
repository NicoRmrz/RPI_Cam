import io
import datetime
from picamera import Color
import logging
from time import sleep
import socketserver
from threading import Condition
from http import server
from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot, QObject, QSize
from picamera.exc import PiCameraValueError, PiCameraMMALError, PiCameraAlreadyRecording

Port_Number = 7227  # Port open on RPI Network
client_list = []         # List of connected users

# PAGE =  index.html 
with open('index.html', 'r') as f:
    PAGE = f.read()
    
class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # New frame, copy the existing buffer's content and notify all
            # clients it's available
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)

class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            self.Update_Clients_Watching()
            
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/j2peg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
                    
                    #To annotate timestamp to stream
                    camera.annotate_text = ("Nico's RPI Cam\n" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

                    # To add current clients tp webpage
                    host, port = self.client_address
                    seen = set(client_list)
                    if host not in seen:
                        seen.add(host)
                        client_list.append(host)
                        self.Update_Clients_Watching()

            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
                    
        #~ elif self.path == '/capture.php':
        
        else:
            self.send_error(404)
            self.end_headers()
            
    def do_POST(self):
        if self.path == '/capture.php':
            Viewers = len(client_list)
            self.newPAGE = PAGE  % (Viewers, client_list)
            content = self.newPAGE.encode('utf-8')
            
            self.send_response(200)
            #~ self.send_header('Content-Type', 'text/php')
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            print("HIIII")
            
            #~ content_length = int(self.headers['Content-Length'])    # <--- Gets the size of data
            #~ post_data = self.rfile.read(content_length)             # <--- Gets the data itself
            #~ logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                    #~ str(self.path), str(self.headers), post_data.decode('utf-8'))
        
        
            #~ self._set_response()
            self.end_headers()
            #~ self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))
            self.wfile.write(content)
            #~ self.Update_Clients_Watching()
        else:
            self.send_error(404)
            self.end_headers()
            
    def Update_Clients_Watching(self):
        Viewers = len(client_list)
        self.newPAGE = PAGE  % (Viewers, client_list)
        content = self.newPAGE.encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', len(content))
        self.end_headers()
        self.wfile.write(content)

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True
    #socketserver.ThreadingMixIn.server_close()

class WebStream_Thread(QThread):
    Web_Stream_signal = pyqtSignal(str)
    
    def __init__(self, RPICamera):
        QThread.__init__(self)
        self.camera = RPICamera
        global camera 
        camera = self.camera
        self.exitProgram = False
        self.Server_Ready = False
        self.Stop_Ready = False
        self.Start_Ready = False
        
    #Sets up the program to exit when the main window is shutting down
    def Set_Exit_Program(self, exiter):
        self.exitProgram = exiter

    #Sets up the program to start web stream
    def StartStreaming(self, Server_Rdy):
        self.Server_Ready = Server_Rdy

    #Sets up the program to stop web stream
    def setStop(self, Stop_Rdy):
        self.Stop_Ready = Stop_Rdy
        rec_status = self.camera.recording   
             
        if (self.Stop_Ready != False and rec_status != False):
            self.camera.stop_recording(splitter_port = 3)
            self.Stop_Ready = False
                    
    #Sets up the program to start web stream
    def setStart(self, Start_Rdy):    
        self.Start_Ready = Start_Rdy 
        rec_status = self.camera.recording
       
        if (self.Start_Ready != False and rec_status != True):
            try:
                self.camera.start_recording(output, format='mjpeg', splitter_port = 3)
                self.camera.annotate_background = Color.from_rgb_bytes(152, 251, 152) 
                self.camera.annotate_foreground = Color('black')
            
            except PiCameraAlreadyRecording as e:
                self.Stream_Out(str(e))
            
            finally:
                self.Start_Ready = False
                    
    
    #Functions runs from .start()
    def run(self):
        self.setPriority(QThread.HighestPriority)

        while (1):
            if (self.Server_Ready != False):
                try:
                    self.camera.start_recording(output, format='mjpeg', splitter_port = 3)
                    self.camera.annotate_background = Color.from_rgb_bytes(152, 251, 152) 
                    self.camera.annotate_foreground = Color('black')

                    address = ('', Port_Number)
                    server = StreamingServer(address, StreamingHandler)
                    #~ print('Starting server, use <Ctrl-C> to stop')
                    self.Stream_Out('Starting server, use <Ctrl-C> to stop')
                              
                    server.serve_forever()
                    
                except PiCameraAlreadyRecording as e: 
                    self.Stream_Out(str(e))
                    #self.Server_Ready = False
                    #~ self.setStop(True)
                    #~ sleep (1)
                    #~ self.setStart(True)
                    
            if(self.exitProgram == True):
                self.exitProgram = False
                break

            sleep(1)       
            
     #Emits the string to console log GUI
    def Stream_Out(self,strm_str):
        self.Web_Stream_signal.emit(strm_str)                          

#Intantiate Global Output Stream and start web streaming
output = StreamingOutput()        

            
           


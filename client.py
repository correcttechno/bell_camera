import cv2
import io
import socket
import struct
import time
import pickle
import numpy as np
import imutils
import pyaudio
import threading

from camera import readCameraFrame


# client_socket.connect(('0.tcp.ngrok.io', 19194))
#HOST = '192.168.0.108'
HOST = '162.214.48.246'
CAMERAPORT = 8095
SOUNDPORT=8094

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 48000
CHUNK_SIZE = 1024

try:
    cameraSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cameraSocket.connect((HOST, CAMERAPORT))
    cameraSocket.send("DOORBELL".encode('utf-8'))
except:
    print("Error camera socket")


try:
    soundSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soundSocket.connect((HOST, SOUNDPORT))
    soundSocket.send("DOORBELL".encode('utf-8'))
except:
    print("Error sound socket")


#encode to jpeg format
#encode param image quality 0 to 100. default:95
#if you want to shrink data size, choose low image quality.






def cameraClient():
    img_counter = 0
    encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),60]
    try:
        while True:
            cleanFrame=readCameraFrame()
            if cleanFrame is not None:
                frame=cleanFrame
                #frame = imutils.resize(frame, width=320,height=240)
            
                frame = cv2.flip(frame,180)
                result, image = cv2.imencode('.jpg', frame, encode_param)
                data = pickle.dumps(image, 0)
                size = len(data)

                if True:
                  
                    if len(data)>0:
                        cameraSocket.sendall(struct.pack(">L", size) + data)
                    #cv2.imshow('client',frame)
                    time.sleep(0.01)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except:
        print("Error camera socket")
    

    


audio = pyaudio.PyAudio()


stream_in = audio.open(format=FORMAT, channels=CHANNELS,
                rate=RATE, input=True,
                frames_per_buffer=CHUNK_SIZE)
    

def soundClient():
    
    while True:
        sounddata = stream_in.read(CHUNK_SIZE,exception_on_overflow=False)
     
        if len(sounddata)>0:
            soundSocket.sendall(sounddata)
           
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
   
        






threading.Thread(target=cameraClient).start()

threading.Thread(target=soundClient).start()
#soundClient()
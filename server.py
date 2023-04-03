# Import the required modules
from io import BytesIO
import io
import socket
import sys
import cv2,struct, base64
import matplotlib.pyplot as plt
import pickle
import numpy as np
import struct ## new
import threading
import zlib
import imutils
from PIL import Image, ImageOps
import asyncio
import websockets
import mediapipe as mp
#import pyaudio
#from pydub import AudioSegment


HOST = '192.168.16.106'
CAMERAPORT = 8091
SOUNDPORT=8092

CHUNK_SIZE = 1024
#FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
SAMPLE_RATE = 44100
SAMPLE_WIDTH = 2


cs=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
cs.bind((HOST,CAMERAPORT))
cs.listen(5)

ss=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ss.bind((HOST,SOUNDPORT))
ss.listen(5)




MYFR=[None,None]
MData=None
MData_Size=None

cameraCLIENTS=[]
soundCLIENTS=[]



#kamera functions

def startCameraBind(index):
    while True:
        conn,addr=cs.accept()
        cameraCLIENTS.append(conn)


def startCamera( index):
    data = b""
    payload_size = struct.calcsize("<L")
    
    while True:
        if len(cameraCLIENTS)>=1:
            print("payload_size: {}".format(payload_size))
            while len(data) < payload_size:
                data += cameraCLIENTS[0].recv(4096)
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("<L", packed_msg_size)[0]

            # Veriyi al
            while len(data) < msg_size:
                data += cameraCLIENTS[0].recv(4096)
            frame_data = data[:msg_size]
            data = data[msg_size:]

            # Veriyi ayrıştırma ve ekranda gösterme
            frame = pickle.loads(frame_data)

            data = np.array(data)
            string_data = data.tostring()
            print(string_data)
            #cv2.imshow('frame', frame)
            #cameraCLIENTS[1].sendall(string_data)

            
            #MYFR[index]=frame
threading.Thread(target=startCamera,args={0}).start()






#p = pyaudio.PyAudio()
#stream_out = p.open(format=FORMAT,
#                                channels=CHANNELS,
#                                rate=RATE,
#                                output=True,
#                                frames_per_buffer=CHUNK_SIZE)



def startSoundBind(index):
    while True:
        conn,addr=ss.accept()
        soundCLIENTS.append(conn)
       
def startSound(index):
    

    while True:
        if len(soundCLIENTS)>=2:
            #print("ISMEL BASLADI")
                    # İstemciden gelen veriyi al
            sounddata = soundCLIENTS[0].recv(CHUNK_SIZE)
            
            #stream_out.write(sounddata)
            

            soundCLIENTS[1].sendall(sounddata)   
            #for c in CLIENTS:
                #c.send(sounddata)               
                
            
threading.Thread(target=startSound,args={0}).start()








cameraServerBind=threading.Thread(target=startCameraBind,args={0})
cameraServerBind.start()


soundServerBind=threading.Thread(target=startSoundBind,args={0})
soundServerBind.start()
#websocket funcktions


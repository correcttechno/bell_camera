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
import pyaudio
from pydub import AudioSegment


HOST = '192.168.16.106'
CAMERAPORT = 8091
SOUNDPORT=8092

CHUNK_SIZE = 512
FORMAT = pyaudio.paInt16
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




#kamera functions
def startCamera( index):
    global MYFR

    conn,addr=cs.accept()

    data = b""
    payload_size = struct.calcsize(">L")
    print("payload_size: {}".format(payload_size))
    while True:
        if conn:
            while len(data) < payload_size:
                data += conn.recv(50*1024)
                MData=data
                if not data:
                    cv2.destroyAllWindows()
                    conn,addr=cs.accept()
                    continue
            # receive image row data form client socket
            packed_msg_size = data[:payload_size]

            data = data[payload_size:]
        
            msg_size = struct.unpack(">L", packed_msg_size)[0]
            while len(data) < msg_size:
                data += conn.recv(50*1024)
            frame_data = data[:msg_size]
            data = data[msg_size:]
            # unpack image using pickle 
            
            frame=pickle.loads(frame_data, fix_imports=True, encoding="bytes")
            frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
            
            #MYFR[index]=frame



CLIENTS=[]
SOUNDTHREAD=[]

def startSoundBind(index):
    while True:
        conn,addr=ss.accept()
        CLIENTS.append(conn)
        print("YENI BAGLANTI")
        print(len(CLIENTS))
        id=len(CLIENTS)-1
        
        



p = pyaudio.PyAudio()
stream_out = p.open(format=FORMAT,
                                channels=CHANNELS,
                                rate=RATE,
                                output=True,
                                frames_per_buffer=CHUNK_SIZE)



def startSound(index):
    global MYFR


    
    while True:
        if len(CLIENTS)>=2:
            print("ISMEL BASLADI")
                    # İstemciden gelen veriyi al
            sounddata = CLIENTS[0].recv(CHUNK_SIZE)
            
            stream_out.write(sounddata)
            

            CLIENTS[1].sendall(sounddata)   
            #for c in CLIENTS:
                #c.send(sounddata)               
                
            
threading.Thread(target=startSound,args={0}).start()






#camera and sound server start
cameraServer = threading.Thread(target=startCamera,args={0})
cameraServer.start()


soundServerBind=threading.Thread(target=startSoundBind,args={0})
soundServerBind.start()
#websocket funcktions


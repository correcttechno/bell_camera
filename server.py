# Import the required modules
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

HOST = '192.168.16.106'
CAMERAPORT = 8091
SOUNDPORT=8092

CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100


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
            
            MYFR[index]=frame




def startSound(index):
    p = pyaudio.PyAudio()
    stream_out = p.open(format=FORMAT,
                                channels=CHANNELS,
                                rate=RATE,
                                output=True,
                                frames_per_buffer=CHUNK_SIZE)
    
    global MYFR
    conn,addr=ss.accept()
    p = pyaudio.PyAudio()

    while True:
        if conn:
            while True:
                # İstemciden gelen veriyi al
                sounddata = conn.recv(CHUNK_SIZE)
                stream_out.write(sounddata)
            
            






#camera and sound server start
cameraServer = threading.Thread(target=startCamera,args={0})
cameraServer.start()

soundServer = threading.Thread(target=startSound,args={0})
soundServer.start()

#websocket funcktions

def startCam( ):
    global MYFR
    global MData_Size
    global MData
    conn,addr=s.accept()
    encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]
    img_counter = 0
    while conn:

        frame = imutils.resize(MYFR[0], width=320)
        # 鏡像
        frame = cv2.flip(frame,180)
        result, image = cv2.imencode('.jpg', frame, encode_param)
        data = pickle.dumps(image, 0)
        size = len(data)

        if img_counter%10==0:
            conn.sendall(struct.pack(">L", size) + data)
            #cv2.imshow('client',frame)
        
    img_counter += 1


        
        #MYFR[index]=frame
       









async def transmit(websocket, path):
    print("Client Connected !")
    try :
        

        while MYFR[0] is not None:
            #encoded = cv2.imencode('.jpg', frame)
            frame = imutils.resize(MYFR[0], width=320)
            frame = cv2.flip(frame,180)
            result, image = cv2.imencode('.jpg', frame)

            data = str(base64.b64encode(image))
            data = data[2:len(data)-1]
            
            await websocket.send(data)
            
            # cv2.imshow("Transimission", frame)
            
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break
       
    except websockets.connection.ConnectionClosed as e:
        print("Client Disconnected !")
        
    except:
        print("Someting went Wrong !")

start_server = websockets.serve(transmit, port=8077)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()


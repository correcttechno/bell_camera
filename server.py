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

HOST='162.214.48.246'
#HOST='192.168.16.106'
PORT=8090

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print('Socket created')

s.bind((HOST,PORT))
print('Socket bind complete')
s.listen(5)
print('Socket now listening')
MYFR=[None,None]
MData=None
MData_Size=None

def startLive( index):
    global MYFR

    conn,addr=s.accept()

    data = b""
    payload_size = struct.calcsize(">L")
    print("payload_size: {}".format(payload_size))
    while True:
        while len(data) < payload_size:
            data += conn.recv(50*1024)
            MData=data
            if not data:
                cv2.destroyAllWindows()
                conn,addr=s.accept()
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
       




p1 = threading.Thread(target=startLive,args={0})
p1.start()




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

start_server = websockets.serve(transmit, port=8093)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()


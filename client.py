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


# client_socket.connect(('0.tcp.ngrok.io', 19194))
#HOST='192.168.16.106'å
HOST = '192.168.16.106'
CAMERAPORT = 8091
SOUNDPORT=8092

CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100


cameraSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cameraSocket.connect((HOST, CAMERAPORT))

soundSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soundSocket.connect((HOST, SOUNDPORT))

cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FPS, 24)


#encode to jpeg format
#encode param image quality 0 to 100. default:95
#if you want to shrink data size, choose low image quality.


def startCamera():
    img_counter = 0
    encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]
    while True:
        ret, frame = cam.read()
        
        encoded, buffer = cv2.imencode('.jpg', frame)
        data = pickle.dumps(buffer)

        # Veri boyutunu hesaplayın ve istemciye gönderin
        message_size = struct.pack("L", len(data))
        cameraSocket.sendall(message_size + data)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        

    cam.release()


def startSound():
    p = pyaudio.PyAudio()
    stream_in = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK_SIZE)
    while True:
        sounddata = stream_in.read(CHUNK_SIZE)
        if len(sounddata)>0:
            soundSocket.sendall(sounddata)
        
        




cameraClient= threading.Thread(target=startCamera)
cameraClient.start()

soundClient= threading.Thread(target=startSound)
soundClient.start()
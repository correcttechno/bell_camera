import cv2
import io
import socket
import struct
import time
import pickle
import numpy as np
import imutils
#import pyaudio
import threading


# client_socket.connect(('0.tcp.ngrok.io', 19194))
#HOST = '192.168.0.108'
HOST = '162.214.48.246'
CAMERAPORT = 8097
SOUNDPORT=8094

CHUNK_SIZE = 128
#FORMAT = pyaudio.paInt16
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
    encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),60]
    while True:
        ret, frame = cam.read()
    
        frame = imutils.resize(frame, width=320,height=240)
    
        frame = cv2.flip(frame,180)
        result, image = cv2.imencode('.jpg', frame, encode_param)
        data = pickle.dumps(image, 0)
        size = len(data)

        if img_counter%2==0:
            if len(data)>0:
                cameraSocket.sendall(struct.pack(">L", size) + data)
            #cv2.imshow('client',frame)
            
        img_counter += 1
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        

    cam.release()


""" def startSound():
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
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break """
        




cameraClient= threading.Thread(target=startCamera)
cameraClient.start()

#soundClient= threading.Thread(target=startSound)
#soundClient.start()
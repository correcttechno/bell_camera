import cv2
import io
import socket
import struct
import time
import pickle
import numpy as np
import imutils
import pyaudio


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client_socket.connect(('0.tcp.ngrok.io', 19194))
#HOST='192.168.16.106'å
#HOST='162.214.48.246'
HOST='192.168.16.106'
PORT=8092
client_socket.connect((HOST, PORT))

cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FPS, 24)
img_counter = 0

#encode to jpeg format
#encode param image quality 0 to 100. default:95
#if you want to shrink data size, choose low image quality.
encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]


CHANNELS = 1
RATE = 44100
CHUNK = 512
FORMAT = pyaudio.paInt16


audio = pyaudio.PyAudio()

# ses verisi için stream açma
stream = audio.open(format=pyaudio.paInt16,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)



stream2 = audio.open(format=FORMAT ,channels=CHANNELS, rate=RATE, output=True)
while True:
    ret, frame = cam.read()
    audio_data = stream.read(CHUNK)

    frame = imutils.resize(frame, width=320)
 
    frame = cv2.flip(frame,180)
    result, image = cv2.imencode('.jpg', frame, encode_param)
    data = pickle.dumps(image, 0)
    size = len(data)


 
    

    #stream2.write(audio_data)
    if img_counter%2==0:
        client_socket.sendall(struct.pack(">L", size) + data)
        #client_socket.sendall(audio_data)
        
        #cv2.imshow('client',frame)
        
    img_counter += 1

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    

cam.release()
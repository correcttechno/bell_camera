from email import utils
import pickle
import socket
import struct
import time
import cv2
import pyaudio
import threading


HOST = '81.17.95.30'  
AUDIOPORT = 8094
VIDEOPORT = 8095
TEXTPORT=8096

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK_SIZE = 4096
cleanFrame = None


audioClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
audioClientSocket.connect((HOST, AUDIOPORT))

videoClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
videoClientSocket.connect((HOST, VIDEOPORT))

textClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#textClientSocket.connect((HOST, TEXTPORT))



audio = pyaudio.PyAudio()
video =None
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 15]

stream_in = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True,
                       input_device_index=11,
                       frames_per_buffer=CHUNK_SIZE)

stream_out = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True,
                        frames_per_buffer=CHUNK_SIZE)
#send audio data
def sendAudio():
    while True:
        data = stream_in.read(CHUNK_SIZE)
        audioClientSocket.sendall(data)
#recive audio data
def receiveAudio():
    while True:
        data = audioClientSocket.recv(CHUNK_SIZE)
        if data:
            stream_out.write(data)
#set camera frame
def setClientCameraFrame(vd):
    global video
    video=vd
#send video data
def sendVideo():
    global video
    while True:
        if video is not None:
          
            success, frame = video.read()
            if True:
                frame = cv2.flip(frame, 180)
                result, image = cv2.imencode('.jpg', frame, encode_param)
                data = pickle.dumps(image, 0)
                size = len(data)
                if len(data) > 0:
                    videoClientSocket.sendall(struct.pack(">L", size) + data)
#send text data
def sendText(MESSAGE):
    textClientSocket.send(MESSAGE.encode())
#recive text data
def receiveText():
    while True:
        data = textClientSocket.recv(1024)
        return data
    
#start functions
threading.Thread(target=sendAudio).start()
threading.Thread(target=receiveAudio).start()
threading.Thread(target=sendVideo).start()
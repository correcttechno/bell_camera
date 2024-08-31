import pickle
import socket
import struct
import time
import cv2
import pyaudio
import threading


HOST = '127.0.0.1'  
AUDIOPORT = 8094
VIDEOPORT = 8095

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK_SIZE = 4096
cleanFrame = None


audioClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
audioClientSocket.connect((HOST, AUDIOPORT))

videoClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
videoClientSocket.connect((HOST, VIDEOPORT))

audio = pyaudio.PyAudio()
#video = cv2.VideoCapture(0)
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 15]

stream_in = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True,
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
def setClientCameraFrame(frame):
    global cleanFrame
    cleanFrame=frame
#send video data
def sendVideo():
    global cleanFrame
    while True:
        #success, cleanFrame = video.read()
        if cleanFrame is not None:
            frame = cleanFrame
            # frame = imutils.resize(frame, width=320,height=240)
            frame = cv2.flip(frame, 180)
            result, image = cv2.imencode('.jpg', frame, encode_param)
            data = pickle.dumps(image, 0)
            size = len(data)
            if len(data) > 0:
                videoClientSocket.sendall(struct.pack(">L", size) + data)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

#start functions
threading.Thread(target=sendAudio).start()
threading.Thread(target=receiveAudio).start()
threading.Thread(target=sendVideo).start()
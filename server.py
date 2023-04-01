import cv2
import numpy as np
import pyaudio
import socket

# video özellikleri
WIDTH = 640
HEIGHT = 480

# ses özellikleri
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK_SIZE = 1024

# soket özellikleri
IP_ADDRESS = '192.168.16.106'
VIDEO_PORT = 5000
AUDIO_PORT = 5001

# video ve ses alıcı soketler
video_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
video_socket.bind((IP_ADDRESS, VIDEO_PORT))

audio_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
audio_socket.bind((IP_ADDRESS, AUDIO_PORT))

# video açma işlemleri
def open_video():
    while True:
        try:
            data, addr = video_socket.recvfrom(65507)
            frame = cv2.imdecode(np.frombuffer(data, dtype=np.uint8), cv2.IMREAD_COLOR)
            cv2.imshow('Video', frame)
            if cv2.waitKey(1) == ord('q'):
                break
        except:
            break

# ses açma işlemleri
def open_audio():
    audio_player = pyaudio.PyAudio()
    audio_stream = audio_player.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True)
    while True:
        try:
            data, addr = audio_socket.recvfrom(CHUNK_SIZE)
            audio_stream.write(data)
        except:
            break

# threading
video_thread = threading.Thread(target=open_video)
audio_thread = threading.Thread(target=open_audio)
video_thread.start()
audio_thread.start()

# main loop
while True:
    pass

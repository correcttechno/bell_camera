import cv2
import numpy as np
import pyaudio
import socket
import threading
import time

# video özellikleri
WIDTH = 640
HEIGHT = 480
FPS = 30

# ses özellikleri
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK_SIZE = 1024

# soket özellikleri
IP_ADDRESS = '192.168.16.106'
VIDEO_PORT = 5000
AUDIO_PORT = 5001

# video sıkıştırıcı
VIDEO_CODEC = cv2.VideoWriter_fourcc(*'H264')
video_writer = cv2.VideoWriter('output.mp4', VIDEO_CODEC, FPS, (WIDTH, HEIGHT))

# ses sıkıştırıcı
audio_encoder = pyaudio.PyAudio()
audio_stream = audio_encoder.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK_SIZE)
audio_chunk = audio_stream.read(CHUNK_SIZE)

# soketler
video_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
audio_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# görüntü kaynağı
capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
capture.set(cv2.CAP_PROP_FPS, FPS)

# video ve ses gönderme işlemleri
def send_video():
    while True:
        ret, frame = capture.read()
        if not ret:
            break
        _, jpeg_frame = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
        video_socket.sendto(jpeg_frame.tobytes(), (IP_ADDRESS, VIDEO_PORT))
        video_writer.write(frame)

def send_audio():
    while True:
        audio_chunk = audio_stream.read(CHUNK_SIZE)
        audio_socket.sendto(audio_chunk, (IP_ADDRESS, AUDIO_PORT))

# threading
video_thread = threading.Thread(target=send_video)
audio_thread = threading.Thread(target=send_audio)
video_thread.start()
audio_thread.start()

# main loop
while True:
    time.sleep(1)

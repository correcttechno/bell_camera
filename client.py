import cv2
import numpy as np
import pyaudio
import socket

# Video ayarları
VIDEO_WIDTH = 640
VIDEO_HEIGHT = 480
VIDEO_FPS = 30

# Ses ayarları
CHUNK_SIZE = 1024
SAMPLE_RATE = 44100
CHANNELS = 1

# Bağlantı ayarları
SERVER_IP = '192.168.16.106'
PORT = 8079

# Kamera ayarları
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, VIDEO_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, VIDEO_HEIGHT)
cap.set(cv2.CAP_PROP_FPS, VIDEO_FPS)

# Ses aygıtı oluştur
audio = pyaudio.PyAudio()
stream = audio.open(format=pyaudio.paInt16, channels=CHANNELS, rate=SAMPLE_RATE, input=True, frames_per_buffer=CHUNK_SIZE)

# Bağlanma
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, PORT))

# Video ve ses akışını başlatma
while True:
    # Video akışını okuma
    ret, frame = cap.read()
    frame = cv2.resize(frame, (VIDEO_WIDTH, VIDEO_HEIGHT))
    data = cv2.imencode('.jpg', frame)[1].tostring()

    # Ses akışını okuma
    audio_data = stream.read(CHUNK_SIZE)

    # Video ve ses akışlarını gönderme
    client_socket.sendall((str(len(data)).ljust(16)).encode('utf-8') + data)
    client_socket.sendall(audio_data)

    # Çıkış için 'q' tuşuna basın
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Temizleme
cap.release()
cv2.destroyAllWindows()
stream.stop_stream()
stream.close()
audio.terminate()
client_socket.close()

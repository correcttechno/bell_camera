import cv2
import numpy as np
import pyaudio
import socket

# Video ayarları
VIDEO_WIDTH = 640
VIDEO_HEIGHT = 480

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

# Ses aygıtı oluştur
audio = pyaudio.PyAudio()
stream = audio.open(format=pyaudio.paInt16, channels=CHANNELS, rate=SAMPLE_RATE, output=True, frames_per_buffer=CHUNK_SIZE)

# Sunucu soketini oluşturma
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_IP, PORT))
server_socket.listen(1)

# İstemciden gelen video ve ses akışını alma
while True:
    # Bağlantıyı kabul etme
    client_socket, address = server_socket.accept()

    # Veri boyutunu okuma
    data_size = client_socket.recv(16)
    data_size = int(data_size.decode('utf-8').strip())

    # Veriyi alın ve yeniden şekillendirin
    data = b''
    while len(data) < data_size:
        packet = client_socket.recv(data_size - len(data))
        if not packet:
            break
        data += packet
    frame = cv2.imdecode(np.frombuffer(data, dtype=np.uint8), cv2.IMREAD_COLOR)

    # Ses verisini okuyun
    audio_data = client_socket.recv(CHUNK_SIZE)

    # Görüntüyü ekranda gösterin ve sesi çalın
    cv2.imshow('Video Stream', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    stream.write(audio_data)

# Temizleme
cap.release()
cv2.destroyAllWindows()
stream.stop_stream()
stream.close()
audio.terminate()
client_socket.close()
server_socket.close()

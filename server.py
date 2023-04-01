import cv2
import pyaudio
import socket
import struct
import numpy as np

# bağlantı parametreleri
IP_ADDRESS = '192.168.16.106'
PORT = 9000

# TCP/IP soketi oluştur
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((IP_ADDRESS, PORT))
server_socket.listen(0)

# Görüntü kodlama ayarları
decode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

# PyAudio ayarları
CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

# PyAudio örneği oluştur
audio = pyaudio.PyAudio()

# Mikrofon çıkışını başlat
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, output=True,
                    frames_per_buffer=CHUNK_SIZE)

while True:
    # Bağlantı isteği al
    client_socket, addr = server_socket.accept()
    # Veri paketi al
    data = b''
    while True:
        packet = client_socket.recv(4096)
        if not packet: break
        data += packet
    # Veri boyutlarını ayrıştır
    video_size = struct.unpack('!L', data[:4])[0]
    audio_size = struct.unpack('!L', data[video_size+4:video_size+8])[0]
    # Görüntüyü ayrıştır ve göster
    frame_encoded = data[4:video_size+4]
    frame = cv2.imdecode(np.fromstring(frame_encoded, dtype=np.uint8), 1)
    cv2.imshow('frame', frame)
    cv2.waitKey(1)
    # Ses verisini ayrıştır ve çal
    audio_data = data[video_size+8:]
    stream.write(audio_data)
    # Soketi kapat
    client_socket.close()

# Kaynakları serbest bırak
server_socket.close()
stream.stop_stream()
stream.close()
audio.terminate()
cv2.destroyAllWindows()

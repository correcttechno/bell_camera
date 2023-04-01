import cv2
import pyaudio
import socket
import struct

# bağlantı parametreleri
IP_ADDRESS = '192.168.16.106'
PORT = 8076

# TCP/IP soketi oluştur
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP_ADDRESS, PORT))

# Kamera akışını başlat
video_capture = cv2.VideoCapture(0)

# Görüntü kodlama ayarları
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

# PyAudio ayarları
CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

# PyAudio örneği oluştur
audio = pyaudio.PyAudio()

# Mikrofon akışını başlat
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK_SIZE)

while True:
    # Görüntü yakala
    ret, frame = video_capture.read()
    # Görüntüyü kodla
    result, frame_encoded = cv2.imencode('.jpg', frame, encode_param)
    # Ses verisi oku
    audio_data = stream.read(CHUNK_SIZE)
    # Veri boyutlarını hesapla
    video_size = struct.pack('!L', len(frame_encoded))
    audio_size = struct.pack('!L', len(audio_data))
    # Verileri bir araya getir ve paketle
    packet = video_size + frame_encoded.tobytes() + audio_size + audio_data
    # Paketi gönder
    client_socket.sendall(packet)

# Kaynakları serbest bırak
video_capture.release()
stream.stop_stream()
stream.close()
audio.terminate()
client_socket.close()

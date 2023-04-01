import io
import socket
import struct
import time
import picamera
import pyaudio

# bağlantı parametreleri
SERVER_IP = '192.168.16.106'
SERVER_PORT =8077

# Raspberry Pi kamera ayarları
RESOLUTION = (640, 480)
FRAMERATE = 24

# ses kayıt ayarları
CHUNK_SIZE = 1024
SAMPLE_RATE = 44100
RECORD_SECONDS = 1

# TCP/IP soketi oluştur
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, SERVER_PORT))

# Kamera örneği oluştur
camera = picamera.PiCamera(resolution=RESOLUTION, framerate=FRAMERATE)

# Ses kayıt cihazı örneği oluştur
audio = pyaudio.PyAudio()
stream = audio.open(format=pyaudio.paInt16, channels=1, rate=SAMPLE_RATE, input=True, frames_per_buffer=CHUNK_SIZE)

# Görüntü akışını ve ses kaydını başlat
video_stream = io.BytesIO()
while True:
    # Görüntüyü al
    camera.capture(video_stream, format='jpeg', use_video_port=True)
    # Görüntü boyutunu al
    video_size = video_stream.tell()
    # Ses verisini al
    audio_data = stream.read(CHUNK_SIZE)
    # Ses verisi boyutunu al
    audio_size = len(audio_data)
    # Görüntüyü ve ses verisini birleştir
    data = struct.pack("!L", video_size) + video_stream.getvalue() + struct.pack("!L", audio_size) + audio_data
    # Veri paketini gönder
    client_socket.sendall(data)
    # Veri akışlarını sıfırla
    video_stream.seek(0)
    video_stream.truncate()

import socket
import pyaudio
import threading

# Sunucu ayarları
HOST = '127.0.0.1'  # Sunucunun IP adresi
PORT = 8094

# Ses ayarları
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK_SIZE = 4096

# İstemci soketi oluşturuluyor
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

audio = pyaudio.PyAudio()

# Giriş (mikrofon) stream
stream_in = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True,
                       frames_per_buffer=CHUNK_SIZE)

# Çıkış (hoparlör) stream
stream_out = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True,
                        frames_per_buffer=CHUNK_SIZE)

def send_audio():
    """Mikrofon verisini sunucuya gönderir"""
    while True:
        data = stream_in.read(CHUNK_SIZE)
        client_socket.sendall(data)

def receive_audio():
    """Sunucudan gelen veriyi hoparlörden çalar"""
    while True:
        data = client_socket.recv(CHUNK_SIZE)
        if data:
            stream_out.write(data)

# İki thread başlatılıyor: biri ses göndermek diğeri almak için
threading.Thread(target=send_audio).start()
threading.Thread(target=receive_audio).start()

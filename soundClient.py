import socket
import pyaudio

# Sunucu bilgileri
HOST = '192.168.16.106'
PORT = 8077

# Ses ayarları
CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

# Socket oluşturma
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Sunucuya bağlanma
    s.connect((HOST, PORT))
    print('Sunucuya bağlandı')

    # PyAudio'yu başlat
    p = pyaudio.PyAudio()
    # Kayıt stream'i oluştur
    stream_in = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK_SIZE)
    # Çalma stream'i oluştur
    stream_out = p.open(format=FORMAT,
                         channels=CHANNELS,
                         rate=RATE,
                         output=True,
                         frames_per_buffer=CHUNK_SIZE)

    # Sonsuz döngü
    while True:
        # Ses verisini al
        data = stream_in.read(CHUNK_SIZE)
        s.sendall(data)
        # Veriyi sunucuya

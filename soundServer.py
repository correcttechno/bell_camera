import socket
import pyaudio

# Sunucu bilgileri
HOST = '192.168.16.106'
PORT = 8092

# Ses ayarları
CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

# Socket oluşturma
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Socket'i bağlama
    s.bind((HOST, PORT))
    # Socket'i dinleme
    s.listen(1)
    print('Sunucu çalışıyor...')

    # İstemci bağlandıktan sonra işlem yap
    conn, addr = s.accept()
    with conn:
        print('İstemci bağlandı:', addr)
        # PyAudio'yu başlat
        p = pyaudio.PyAudio()
        # Çalma stream'i oluştur
        stream_out = p.open(format=FORMAT,
                             channels=CHANNELS,
                             rate=RATE,
                             output=True,
                             frames_per_buffer=CHUNK_SIZE)
        # Kayıt stream'i oluştur
        stream_in = p.open(format=FORMAT,
                            channels=CHANNELS,
                            rate=RATE,
                            input=True,
                            frames_per_buffer=CHUNK_SIZE)

        # Sonsuz döngü
        while True:
            # İstemciden gelen veriyi al
            data = conn.recv(CHUNK_SIZE)
            # Veri boş ise döngüyü sonlandır
            if not data:
                break
            # Veriyi çal
            stream_out.write(data)
            # Kaydet
         

            if len(data)>0:
                print("SES geliyor")

        # Stream'leri durdur ve PyAudio'yu kapat
        stream_out.stop_stream()
        stream_out.close()
        stream_in.stop_stream()
        stream_in.close()
        p.terminate()

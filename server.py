import socket
import threading

import pyaudio

audio = pyaudio.PyAudio()

stream_out = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, output=True)




# Sunucu ayarları
HOST = '0.0.0.0'  # Sunucu tüm IP adreslerinden gelen bağlantıları kabul eder.
PORT = 8094

# İstemcileri takip etmek için bir liste
clients = []

# Sunucu soketi oluşturuluyor
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)
print(f"Server started on {HOST}:{PORT}")

def broadcast(data, conn):
    stream_out.write(data)
    """Bir istemciden gelen veriyi diğer tüm istemcilere gönderir"""
    for client in clients:
        if client != conn:
            try:
                client.sendall(data)
            except:
                clients.remove(client)

def handle_client(conn, addr):
    """Her istemci bağlantısı için bu fonksiyon çalışır"""
    print(f"New connection from {addr}")
    clients.append(conn)
    
    while True:
        try:
            data = conn.recv(4096)  # Veriyi al
            if not data:
                break
            broadcast(data, conn)  # Veriyi diğer istemcilere gönder
        except:
            break
    
    # İstemci bağlantısı kesildiğinde
    print(f"Connection from {addr} closed")
    clients.remove(conn)
    conn.close()

def start_server():
    """Sunucuyu başlatır ve istemcilerden gelen bağlantıları kabul eder"""
    while True:
        conn, addr = server.accept()  # Yeni bir bağlantı kabul edilir
        threading.Thread(target=handle_client, args=(conn, addr)).start()
        

# Sunucuyu başlat
start_server()

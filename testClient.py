import socket
import threading
import pyaudio

HEADER_LENGTH = 10
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 48000
CHUNK_SIZE = 4096

def receive_messages(client_socket, stream_out):
    while True:
        try:
            message_header = client_socket.recv(HEADER_LENGTH)
            if not len(message_header):
                break
            message_length = int(message_header.decode('utf-8').strip())
            message = client_socket.recv(message_length)
            stream_out.write(message)
        except Exception as e:
            print(f"Server bağlantısı kesildi: {e}")
            client_socket.close()
            break

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect(('127.0.0.1', 8094))
    except Exception as e:
        print(f"Sunucuya bağlanılamadı: {e}")
        return

    username = input("Kullanıcı adınızı girin: ")
    username = username.encode('utf-8')
    username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
    client.send(username_header + username)

    p = pyaudio.PyAudio()
    
    # Mikrofon için ayarlar
    stream_in = p.open(format=FORMAT,
                       channels=CHANNELS,
                       rate=RATE,
                       input=True,
                       frames_per_buffer=CHUNK_SIZE)

    # Hoparlör için ayarlar
    stream_out = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        output=True,
                        frames_per_buffer=CHUNK_SIZE)

    thread = threading.Thread(target=receive_messages, args=(client, stream_out))
    thread.start()

    try:
        while True:
            data = stream_in.read(CHUNK_SIZE)
            message_header = f"{len(data):<{HEADER_LENGTH}}".encode('utf-8')
            client.send(message_header + data)
    except Exception as e:
        print(f"Hata: {e}")
    finally:
        client.close()
        stream_in.stop_stream()
        stream_in.close()
        stream_out.stop_stream()
        stream_out.close()
        p.terminate()

if __name__ == "__main__":
    start_client()

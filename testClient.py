import socket
import threading
import pyaudio

HEADER_LENGTH = 10

def receive_messages(client_socket, stream_out):
    while True:
        try:
            message_header = client_socket.recv(HEADER_LENGTH)
            if not len(message_header):
                break
            message_length = int(message_header.decode('utf-8').strip())
            message = client_socket.recv(message_length)
            stream_out.write(message)
        except:
            print("Server bağlantısı kesildi.")
            client_socket.close()
            break

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('192.168.16.103', 8094))

    username = input("Kullanıcı adınızı girin: ")
    username = username.encode('utf-8')
    username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
    client.send(username_header + username)

    p = pyaudio.PyAudio()
    
    # Mikrofon için ayarlar
    stream_in = p.open(format=pyaudio.paInt16,
                       channels=1,
                       rate=44100,
                       input=True,
                       frames_per_buffer=1024)

    # Hoparlör için ayarlar
    stream_out = p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=44100,
                        output=True,
                        frames_per_buffer=1024)

    thread = threading.Thread(target=receive_messages, args=(client, stream_out))
    thread.start()

    while True:
        data = stream_in.read(1024)
        message_header = f"{len(data):<{HEADER_LENGTH}}".encode('utf-8')
        client.send(message_header + data)

    client.close()

if __name__ == "__main__":
    start_client()

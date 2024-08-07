import socket
import pyaudio
import threading

# Audio settings
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 48000
CHUNK_SIZE = 4096

# Socket settings
IP = "192.168.16.103"
PORT = 8094

# Create a socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((IP, PORT))
server_socket.listen(2)

print(f"Server listening on {IP}:{PORT}")

clients = []

def handle_client(client_socket, addr):
    global clients
    print(f"Connection from {addr}")
    while True:
        try:
            data = client_socket.recv(CHUNK_SIZE)
            if not data:
                break
            for client in clients:
                if client != client_socket:
                    client.sendall(data)
        except ConnectionResetError:
            break

    clients.remove(client_socket)
    client_socket.close()
    print(f"Connection closed from {addr}")

# Accept clients
while len(clients) < 2:
    client_socket, addr = server_socket.accept()
    clients.append(client_socket)
    client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
    client_thread.start()

import socket
import threading

HEADER_LENGTH = 10
clients = {}

def handle_client(client_socket, addr):
    print(f"Yeni bağlantı: {addr}")
    
    try:
        username_header = client_socket.recv(HEADER_LENGTH)
        username_length = int(username_header.decode('utf-8').strip())
        username = client_socket.recv(username_length).decode('utf-8')
        clients[client_socket] = username
        print(f"Kullanıcı adı {username} olarak belirlendi.")
    except:
        client_socket.close()
        return

    while True:
        try:
            message_header = client_socket.recv(HEADER_LENGTH)
            if not len(message_header):
                break
            message_length = int(message_header.decode('utf-8').strip())
            message = client_socket.recv(message_length)

            broadcast(message, client_socket)
        except:
            clients.pop(client_socket, None)
            client_socket.close()
            print(f"Bağlantı kesildi: {addr}")
            break

def broadcast(message, current_client):
    for client in clients:
        if client != current_client:
            try:
                client.send(message)
            except:
                clients.pop(client, None)
                client.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 8094))
    server.listen(5)  # Daha fazla client'ı destekleyebilir
    print("Server dinleniyor...")

    while True:
        client_socket, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        thread.start()

if __name__ == "__main__":
    start_server()

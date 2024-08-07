import socket
import threading

HEADER_LENGTH = 10

def receive_messages(client_socket):
    while True:
        try:
            message_header = client_socket.recv(HEADER_LENGTH)
            if not len(message_header):
                break
            message_length = int(message_header.decode('utf-8').strip())
            message = client_socket.recv(message_length).decode('utf-8')
            print(message)
        except:
            print("Server bağlantısı kesildi.")
            client_socket.close()
            break

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 5555))

    username = input("Kullanıcı adınızı girin: ")
    username = username.encode('utf-8')
    username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
    client.send(username_header + username)

    thread = threading.Thread(target=receive_messages, args=(client,))
    thread.start()

    while True:
        message = input("")
        if message.lower() == 'exit':
            break
        message = message.encode('utf-8')
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
        client.send(message_header + message)

    client.close()

if __name__ == "__main__":
    start_client()

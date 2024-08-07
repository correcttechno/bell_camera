import socket
import select

# Sunucu bilgileri
HOST = '127.0.0.1'
PORT = 65432

# Sunucu socket oluşturma ve ayarlarını yapma
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen()

# Açık soketleri takip eden liste
sockets_list = [server_socket]

# Kullanıcı adlarıyla eşleşen socket bağlantılarını takip eden dictionary
clients = {}

print(f"Listening for connections on {HOST}:{PORT}...")

def receive_message(client_socket):
    try:
        message_header = client_socket.recv(10)
        if not len(message_header):
            return False
        message_length = int(message_header.decode('utf-8').strip())
        return {'header': message_header, 'data': client_socket.recv(message_length)}
    except:
        return False

while True:
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

    for notified_socket in read_sockets:
        if notified_socket == server_socket:
            client_socket, client_address = server_socket.accept()
            user = receive_message(client_socket)
            if user is False:
                continue

            user_name = user['data'].decode('utf-8')
            sockets_list.append(client_socket)
            clients[client_socket] = user_name

            print(f"Accepted new connection from {client_address[0]}:{client_address[1]} username:{user_name}")

        else:
            message = receive_message(notified_socket)
            if message is False:
                user_name = clients[notified_socket]
                print(f"Closed connection from {user_name}")
                sockets_list.remove(notified_socket)
                del clients[notified_socket]
                continue

            user_name = clients[notified_socket]
            print(f"Received message from {user_name}: {message['data'].decode('utf-8')}")

            # Mesaj formatı: "@username mesaj"
            message_content = message['data'].decode('utf-8')
            if message_content.startswith('@'):
                target_username, message_text = message_content.split(' ', 1)
                target_username = target_username[1:]

                target_socket = None
                for sock, uname in clients.items():
                    if uname == target_username:
                        target_socket = sock
                        break

                if target_socket:
                    target_socket.send(f"{user_name}: {message_text}".encode('utf-8'))
                else:
                    notified_socket.send(f"User {target_username} not found.".encode('utf-8'))
            else:
                # Mesajı tüm client'lara gönder
                for client_socket in clients:
                    if client_socket != notified_socket:
                        client_socket.send(f"{user_name}: {message_content}".encode('utf-8'))

    for notified_socket in exception_sockets:
        sockets_list.remove(notified_socket)
        del clients[notified_socket]

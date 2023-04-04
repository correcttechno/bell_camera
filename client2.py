import cv2
import socket
import struct
import numpy as np

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the server's IP address and port
server_address = ('192.168.0.108', 8097)
sock.connect(server_address)

# Receive size of image


# Receive image data
img_bytes = b''
if True:
    size = struct.unpack('>I', sock.recv(4))[0]
    
    while len(img_bytes) < size:
        img_bytes += sock.recv(4096)

    # Decode image data
    img_np = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(img_np, cv2.IMREAD_COLOR)

    # Display image
    cv2.imshow('Received image', img)
    cv2.waitKey(0)

# Close the socket
#sock.close()

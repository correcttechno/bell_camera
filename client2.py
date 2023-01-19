import cv2
import io
import socket
import struct
import time
import pickle
import numpy as np
import imutils


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client_socket.connect(('0.tcp.ngrok.io', 19194))
client_socket.connect(('162.214.48.246', 8090))


#encode to jpeg format
#encode param image quality 0 to 100. default:95
#if you want to shrink data size, choose low image quality.
encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]
data = b""
if True:
    
    ata = b""
    payload_size = struct.calcsize(">L")
    print("payload_size: {}".format(payload_size))
    while True:
        while len(data) < payload_size:
            print("Data geldi")
            data += client_socket.recv(20*1024)
            
        # receive image row data form client socket
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack(">L", packed_msg_size)[0]
        while len(data) < msg_size:
            print("Data geldi 2")
            data += client_socket.recv(20*1024)
        print("Data geldi 3")
        frame_data = data[:msg_size]
        data = data[msg_size:]
        # unpack image using pickle 
        frame=pickle.loads(frame_data, fix_imports=True, encoding="bytes")
        frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
        
        cv2.imshow('CLIENT',frame)
        cv2.waitKey(1)
        

cam.release()
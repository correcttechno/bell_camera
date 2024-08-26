import pickle
import socket
import socketserver
import struct
import threading

import cv2

#import pyaudio

#audio = pyaudio.PyAudio()

#stream_out = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, output=True)
#stream_in = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True,frames_per_buffer=4096)

HOST = '0.0.0.0' 
AUDIOPORT = 8094
VIDEOPORT = 8095

audioClients = []
videoClients = []

audioServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
audioServer.bind((HOST, AUDIOPORT))
audioServer.listen(5)

videoServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
videoServer.bind((HOST, VIDEOPORT))
videoServer.listen(5)

#Audio Server
def audioBroadcast(data, conn):
    #stream_out.write(data)
    for client in audioClients:
        if client != conn:
            try:
                client.sendall(data)
            except:
               audioClients.remove(client)
#audio handle
def audioHandleClient(conn, addr):
    print(f"New connection from {addr}")
    audioClients.append(conn)
    
    while True:
        try:
            data = conn.recv(4096)  
            if not data:
                break
            audioBroadcast(data, conn)  
        except:
            break
    
    print(f"Connection from {addr} closed")
    audioClients.remove(conn)
    conn.close()
#start audio server
def startAudioServer():
    while True:
        conn, addr = audioServer.accept() 
        threading.Thread(target=audioHandleClient, args=(conn, addr)).start()
        

#video Server
def videoBroadcast(data, conn):
    #stream_out.write(data)
    for client in videoClients:
        if client != conn:
            try:
                client.sendall(data)
            except:
               videoClients.remove(client)
#video handle
def videoHandleClient(conn, addr):

    print(f"New connection from {addr}")
    videoClients.append(conn)

    data = b""
    payload_size = struct.calcsize(">L")
    encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]
    while True:
        try:
            while len(data) < payload_size:
                data += conn.recv(50*1024)
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack(">L", packed_msg_size)[0]
            while len(data) < msg_size:
                data += conn.recv(50*1024)
            frame_data = data[:msg_size]
            data = data[msg_size:]
            frame=pickle.loads(frame_data, fix_imports=True, encoding="bytes")
            frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
            frame = cv2.flip(frame,180)
            result, image = cv2.imencode('.jpg', frame, encode_param)
            if conn is not None:
                mydata = struct.pack('>L', len(image.tobytes())) + image.tobytes()
                videoBroadcast(mydata, conn)
        except:
            break
            
    print(f"Connection from {addr} closed")
    videoClients.remove(conn)
    conn.close()
#start video server
def startVideoServer():
    while True:
        conn, addr = videoServer.accept() 
        threading.Thread(target=videoHandleClient, args=(conn, addr)).start()
        

#start servers
threading.Thread(target=startAudioServer).start()
threading.Thread(target=startVideoServer).start()

print("AUDIO SERVER STARTED")
print("VIDEO SERVER STARTED")





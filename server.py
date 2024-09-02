import pickle
import socket
import socketserver
import struct
import threading

import cv2
from flask import json
import requests

#import pyaudio

#audio = pyaudio.PyAudio()

#stream_out = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, output=True)
#stream_in = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True,frames_per_buffer=4096)

HOST = '0.0.0.0' 
AUDIOPORT = 8094
VIDEOPORT = 8095
TEXTPORT = 8096

audioClients = []
videoClients = []
textClients=[]

audioServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
audioServer.bind((HOST, AUDIOPORT))
audioServer.listen(5)

videoServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
videoServer.bind((HOST, VIDEOPORT))
videoServer.listen(5)

textServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
textServer.bind((HOST, TEXTPORT))
textServer.listen(5)

#send noft
myToken="ea80EBvNQqCMGu907dofEa:APA91bFfrtsQMkuHBGZeSdUTbU0MTzmV6Fj9pV_HgIkD402XGE4E-aTFt6lCZT1B-FO0ABDhNHMGqDZ7xgr0rvMtWq2T9cQ1NoXU3WT-KbT2hjm1Im7gcl55r6lF0lrE2xegSo5HdGoe"
def send_notification(token, title, description, data=None, action='MESSAGING_EVENT'):
    api_key = "AAAAaNeZ-Ok:APA91bGfED82PlJgTTkuuZGLsDJznXvQ88trskAfl2JOPuKE1Dc9TQDM475TnMxx0TYiHPGIgiRnxACjhkJjwy80mSZrj_BbGZ8Lymx2WhDrrs660o_alHb76Uwqmbv4T_FEj7iBNcRb"
    
    registration_ids = [token]
    
    # Mesajı hazırlama
    msg = {
        'body': description,
        'title': title,
        'clickAction': action
    }

    # Veri alanını ekleyelim
    fields = {
        "collapse_key": "type_a",
        'registration_ids': registration_ids,
        'notification': msg,
    }

    if data:
        fields['data'] = data

    headers = {
        'Authorization': 'key=' + api_key,
        'Content-Type': 'application/json'
    }

    response = requests.post('https://fcm.googleapis.com/fcm/send', headers=headers, data=json.dumps(fields))
    
    if response.status_code == 200:
        return response.json().get('success', 0)
    else:
        return 0


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

#Text Server
def textBroadcast(data, conn):
    #stream_out.write(data)
    for client in textClients:
        if client != conn:
            try:
                client.sendall(data)
            except:
               textClients.remove(client)
#text handle
def textHandleClient(conn, addr):
    print(f"New connection from {addr}")
    textClients.append(conn)
    
    while True:
        try:
            data = conn.recv(1024)  
            if not data:
                break
            
            if(data.decode()=="BELL"):
                send_notification(myToken,"SALAM","BELL")
                print("NOFT GONDERILDI")
            #textBroadcast(data, conn)  
        except:
            break
    
    print(f"Connection from {addr} closed")
    textClients.remove(conn)
    conn.close()
#start text server
def startTextServer():
    while True:
        conn, addr = textServer.accept() 
        threading.Thread(target=textHandleClient, args=(conn, addr)).start()
        

#start servers
threading.Thread(target=startAudioServer).start()
threading.Thread(target=startVideoServer).start()
threading.Thread(target=startTextServer).start()

print("AUDIO SERVER STARTED")
print("VIDEO SERVER STARTED")
print("TEXT SERVER STARTED")



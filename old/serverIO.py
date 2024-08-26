import io
import pickle
import time
import cv2
import numpy as np
import socketio
import eventlet
import eventlet.wsgi

# SocketIO sunucusu ve uygulaması oluştur
sio = socketio.Server()
app = socketio.WSGIApp(sio)

# PyAudio ile ses çıkışı ayarları
#p = pyaudio.PyAudio()
#stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, output=True)


clients = []

@sio.event
def connect(sid, environ):
    print(f"Client {sid} connected.")
    clients.append(sid)

@sio.event
def disconnect(sid):
    print(f"Client {sid} disconnected.")
    clients.remove(sid)

@sio.event
def audio_data(sid, data):
    # Veriyi hoparlörde çal
    #stream.write(data)
    
    for client_sid in clients:
        if client_sid != sid:
            sio.emit('audio_data', data, room=client_sid)

@sio.event
def video_data(sid, data):

    """ img_bytes = io.BytesIO(data)
    img_np = np.array(bytearray(img_bytes.read()), dtype=np.uint8)
    img = cv2.imdecode(img_np, cv2.IMREAD_COLOR)
 
    if img is not None:
        cv2.waitKey()"""
    
    for client_sid in clients:
        if client_sid != sid:
            sio.emit('video_data', data, room=client_sid)

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 8094)), app)

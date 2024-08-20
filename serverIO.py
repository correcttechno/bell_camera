import socketio
import pyaudio
import numpy as np

sio = socketio.Server()

# PyAudio ayarları
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=16000,
                output=True)

@sio.event
def connect(sid, environ):
    print('Client connected:', sid)

@sio.event
def disconnect(sid):
    print('Client disconnected:', sid)

@sio.event
def audio_data(sid, data):
    print('Received audio data of length:', len(data))
    # Gelen ses verisini anlık olarak hoparlörden çıkış al
    stream.write(data)

if __name__ == '__main__':
    import eventlet
    import eventlet.wsgi
    from flask import Flask

    # Flask uygulaması oluşturma
    app = Flask(__name__)

    # SocketIO WSGI uygulaması ile Flask uygulamasını birleştirme
    app = socketio.WSGIApp(sio, app)

    # Sunucuyu başlatma
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 5000)), app)

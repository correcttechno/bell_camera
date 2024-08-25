import socketio
import pyaudio

# SocketIO sunucusunu oluştur
sio = socketio.Server()
app = socketio.WSGIApp(sio)

# PyAudio ile ses çıkışı ayarları
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, output=True)

# İstemciden gelen ses verilerini hoparlörde oynat
@sio.event
def audio_data(sid, data):
    stream.write(data)

if __name__ == '__main__':
    import eventlet
    import eventlet.wsgi

    eventlet.wsgi.server(eventlet.listen(('', 8094)), app)

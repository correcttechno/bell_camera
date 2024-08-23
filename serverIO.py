import socketio
import pyaudio
import wave

# Socket.IO istemcisi oluşturun
sio = socketio.Server()
app = socketio.WSGIApp(sio)

# PyAudio ayarları
p = pyaudio.PyAudio()
rate = 44100  # Örnekleme hızı
channels = 1  # Kanal sayısı (mono)
format = pyaudio.paInt16  # PCM16 formatı

# WAV dosyasını yazmak için ayarları yapın
wav_file = wave.open('output.wav', 'wb')
wav_file.setnchannels(channels)
wav_file.setsampwidth(p.get_sample_size(format))
wav_file.setframerate(rate)

@sio.event
def connect(sid, environ):
    print(f"Client connected: {sid}")

@sio.event
def disconnect(sid):
    print(f"Client disconnected: {sid}")

@sio.event
def audio_data(sid, data):
    # Gelen PCM16 formatındaki ses verisini WAV dosyasına yazın
    wav_file.writeframes(data)

if __name__ == '__main__':
    import eventlet
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 5000)), app)

    # Server kapatıldığında WAV dosyasını kapatın
    wav_file.close()

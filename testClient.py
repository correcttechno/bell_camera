import socketio
import pyaudio

# SocketIO istemcisini oluştur
sio = socketio.Client()

# PyAudio ile ses giriş ayarları
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)

# Sunucuya bağlan
sio.connect('http://127.0.0.1:5000')

# Ses verisini mikrofondan alıp sunucuya gönder
def send_audio():
    try:
        while True:
            data = stream.read(1024)
            sio.emit('audio_data', data)
    except KeyboardInterrupt:
        pass
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()
        sio.disconnect()

if __name__ == '__main__':
    send_audio()

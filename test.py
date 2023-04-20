import pyaudio
import pulsectl

p = pyaudio.PyAudio()

# PulseAudio client instance oluşturun
pulse = pulsectl.Pulse('my-client-name')

# Kayıt için PulseAudio stream oluşturun
stream = pulse.record_stream('cart 2')

# Kayıt için PyAudio stream oluşturun
stream_py = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, input_device_index=None, frames_per_buffer=1024, stream_callback=None)

# Kayıt işlemini başlatın
stream_py.start_stream()
stream.start()

# Kaydedilen ses verilerini işleyin
while True:
    data = stream.read(1024)
    stream_py.write(data)

# Kayıt işlemini sonlandırın
stream_py.stop_stream()
stream_py.close()
p.terminate()

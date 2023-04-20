import pyaudio
import wave
 
# Ses özellikleri
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 48000
CHUNK = 1024
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "test.wav"
 
audio = pyaudio.PyAudio()
 
# Ses kaydedici
stream = audio.open(format=FORMAT, channels=CHANNELS,
                rate=RATE, input=True,
                frames_per_buffer=CHUNK)
stream_out = audio.open(format=FORMAT, channels=CHANNELS,
                rate=RATE,output=True,
                frames_per_buffer=CHUNK)
print("Kaydediliyor...")
 
frames = []
 
while True:
    data = stream.read(CHUNK)
    stream_out.write(data)
    //frames.append(data)
 
print("Kayit bitti.")
 
stream.stop_stream()
stream.close()
audio.terminate()
 
# Ses dosyasını kaydet
waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
waveFile.setnchannels(CHANNELS)
waveFile.setsampwidth(audio.get_sample_size(FORMAT))
waveFile.setframerate(RATE)
waveFile.writeframes(b''.join(frames))
waveFile.close()

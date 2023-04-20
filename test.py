import pyaudio
import cv2
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 48000
CHUNK_SIZE = 1024
RECORD_SECONDS = 5
 
audio = pyaudio.PyAudio()
 
# Ses kaydedici
stream_in = audio.open(format=FORMAT, channels=CHANNELS,
                rate=RATE, input=True,
                frames_per_buffer=CHUNK_SIZE)

sounddata = stream_in.read(CHUNK_SIZE)

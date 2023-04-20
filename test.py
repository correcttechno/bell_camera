import pyaudio
import cv2
CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 48000


p = pyaudio.PyAudio()
stream_in = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK_SIZE,
                        input_device_index=1
                        )


sounddata = stream_in.read(CHUNK_SIZE)

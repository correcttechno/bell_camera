import pyaudio

CHUNK_SIZE = 128
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100


p = pyaudio.PyAudio()
stream_in = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK_SIZE,
                        input_device_index=1
                        )
    
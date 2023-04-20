import pyaudio
import cv2
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
                        input_device_index=2
                        )
stream_out = p.open(format=FORMAT,
                               channels=CHANNELS,
                               rate=RATE,
                               output=True,
                               frames_per_buffer=CHUNK_SIZE,
                               output_device_index=2
                               )
while True:
        sounddata = stream_in.read(CHUNK_SIZE)
        stream_out.write(sounddata)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
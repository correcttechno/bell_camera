import alsaaudio
import numpy as np

# Set up audio input
inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NORMAL)
inp.setchannels(1)
inp.setrate(44100)
inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
inp.setperiodsize(1024)

while True:
    # Read data from audio input
    length, data = inp.read()
    # Convert data to numpy array
    data = np.frombuffer(data, dtype=np.int16)
    # Process data as needed
    print(data)

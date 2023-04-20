import alsaaudio
import numpy as np


card = 'sysdefault:CARD=Device [USB Audio Device]' # Örneğin: 'sysdefault:CARD=Device'
device = alsaaudio.PCM_CAPTURE
channels = 1
format = alsaaudio.PCM_FORMAT_S16_LE
rate = 44100

inp = alsaaudio.PCM(device=device, card=card)
inp.setchannels(channels)
inp.setrate(rate)
inp.setformat(format)
inp.setperiodsize(1024)


while True:
    # Read data from audio input
    length, data = inp.read()
    # Convert data to numpy array
    data = np.frombuffer(data, dtype=np.int16)
    # Process data as needed
    print(data)

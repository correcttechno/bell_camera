import asyncio
import websockets
import pyaudio
import numpy as np

# Sabitler
CHUNK_SIZE = 1024
SAMPLE_RATE = 44100
NUM_CHANNELS = 1

async def audio_client():
    # PyAudio'yu başlat
    audio = pyaudio.PyAudio()

    # Ses verisi için bir stream aç
    stream = audio.open(format=pyaudio.paInt16,
                        channels=NUM_CHANNELS,
                        rate=SAMPLE_RATE,
                        output=True)

    async with websockets.connect("ws://192.168.16.103:8077") as websocket:
        while True:
            # Sunucudan ses verisini al
            data = await websocket.recv()

            # Byte dizisini numpy dizisine dönüştür
            audio_data = np.frombuffer(data, dtype=np.int16)

            # Ses verisini işle veya çal
            # ...

            # Ses verisini çıkış stream'ine yaz
            stream.write(audio_data.tobytes())

asyncio.run(audio_client())

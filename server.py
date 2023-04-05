import asyncio
import websockets
import pyaudio
import numpy as np

# Sabitler
CHUNK_SIZE = 1024
SAMPLE_RATE = 44100
NUM_CHANNELS = 1

async def audio_stream(websocket, path):
    # PyAudio'yu başlat
    audio = pyaudio.PyAudio()

    # Ses verisi için bir stream aç
    stream = audio.open(format=pyaudio.paInt16,
                        channels=NUM_CHANNELS,
                        rate=SAMPLE_RATE,
                        input=True,
                        frames_per_buffer=CHUNK_SIZE)

    while True:
        # Ses verisini al
        data = stream.read(CHUNK_SIZE)

        # Ses verisini işle veya kaydet
        # ...

        # Ses verisini WebSocket istemcisine gönder
        await websocket.send(data)

async def main():
    async with websockets.serve(audio_stream, "192.168.16.103", 8077):
        await asyncio.Future()  # Sunucu sonsuza kadar çalışır

asyncio.run(main())

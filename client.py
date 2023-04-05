import cv2
import numpy as np
import pyaudio
import asyncio
import websockets

# Kamera örneğini oluştur
cap = cv2.VideoCapture(0)

# PyAudio örneği oluştur
audio = pyaudio.PyAudio()

# Mikrofon için giriş cihazını aç
stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)

async def video_stream(websocket, path):
    while True:
        # Kameradan bir kare oku
        ret, frame = cap.read()

        # Kareyi JPEG formatına dönüştür ve byte dizisine kodla
        _, img_encoded = cv2.imencode('.jpg', frame)
        data = img_encoded.tobytes()

        # Byte dizisini istemciye gönder
        await websocket.send(data)

async def audio_stream(websocket, path):
    while True:
        # Mikrofondan ses verisini al
        data = stream.read(1024)

        # Ses verisini istemciye gönder
        await websocket.send(data)

async def main():
    async with websockets.connect('ws://192.168.16.103:8077/video') as video_socket, \
            websockets.connect('ws://192.168.16.103:8078/audio') as audio_socket:
        await asyncio.gather(
            video_stream(video_socket, '/video'),
            audio_stream(audio_socket, '/audio')
        )

# Ana programı çalıştır
asyncio.run(main())

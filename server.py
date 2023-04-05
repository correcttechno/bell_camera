import asyncio
import websockets
import cv2
import numpy as np
import pyaudio

# Pencereyi aç
cv2.namedWindow('Video', cv2.WINDOW_NORMAL)

# PyAudio örneği oluştur
audio = pyaudio.PyAudio()

# Hoparlör için çıkış cihazını aç
stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, output=True)

async def video_stream(websocket, path):
    while True:
        # İstemciden gelen görüntüyü al
        data = await websocket.recv()

        # Görüntü verisini numpy dizisine dönüştür
        img_array = np.frombuffer(data, dtype=np.uint8)

        # Diziyi 3 kanallı görüntüye dönüştür
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

        # Görüntüyü ekranda göster
        cv2.imshow('Video', img)
        cv2.waitKey(1)

async def audio_stream(websocket, path):
    while True:
        # İstemciden gelen ses verisini al
        data = await websocket.recv()

        # Sunucuda ses verisini oynat
        stream.write(data)

async def main():
    async with websockets.serve(video_stream, '192.168.16.103', 8077, subprotocols=['video']) as video_server, \
            websockets.serve(audio_stream, '192.168.16.103', 8078, subprotocols=['audio']) as audio_server:
        await asyncio.gather(video_server.wait_closed(), audio_server.wait_closed())

# Ana programı çalıştır
asyncio.run(main())

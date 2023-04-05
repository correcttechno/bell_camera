import cv2
import pyaudio
import numpy as np
import threading
import websocket
import json

# Video capture object
cap = cv2.VideoCapture(0)

# Audio recording object
audio = pyaudio.PyAudio()
stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)

# WebSocket client
ws = websocket.WebSocket()

def send_data():
    while True:
        # Capture video frame
        ret, frame = cap.read()
        if not ret:
            break

        # Record audio frame
        audio_frame = stream.read(1024)

        # Combine video and audio frames into a JSON object
        data = {'video': frame.tolist(), 'audio': np.frombuffer(audio_frame, dtype=np.int16).tolist()}
        json_data = json.dumps(data)

        # Send the JSON object to the WebSocket server
        ws.send(json_data)

def on_open(ws):
    # Start the thread that sends data to the WebSocket server
    threading.Thread(target=send_data).start()

if __name__ == '__main__':
    # Connect to the WebSocket server
    ws.connect('ws://192.168.16.103:8077')

    # Set the on_open callback function
    ws.on_open = on_open

    # Wait for the WebSocket connection to close
    ws.run_forever()

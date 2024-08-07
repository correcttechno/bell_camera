import socket
import pyaudio
import threading

# Audio settings
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 48000
CHUNK_SIZE = 4096

# Socket settings
IP = "192.168.16.103"
PORT = 8094

# Create a socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))

audio = pyaudio.PyAudio()

# Initialize microphone stream
mic_stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK_SIZE)

# Initialize speaker stream
speaker_stream = audio.open(format=FORMAT, channels=CHANNELS,
                            rate=RATE, output=True,
                            frames_per_buffer=CHUNK_SIZE)

def send_audio():
    while True:
        data = mic_stream.read(CHUNK_SIZE)
        client_socket.sendall(data)

def receive_audio():
    while True:
        data = client_socket.recv(CHUNK_SIZE)
        speaker_stream.write(data)

# Start sending and receiving threads
send_thread = threading.Thread(target=send_audio)
receive_thread = threading.Thread(target=receive_audio)

send_thread.start()
receive_thread.start()

send_thread.join()
receive_thread.join()

import pickle
import struct
import threading
import cv2
import socketio
import pyaudio

sio = socketio.Client()

sio.connect('http://81.17.95.30:8094')
#sio.connect('http://127.0.0.1:8094')

p = pyaudio.PyAudio()
input_stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
output_stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, output=True, frames_per_buffer=1024)

cap = cv2.VideoCapture(0)
encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),15]


@sio.event
def send_video():
    try:
        print("VIDEO GEDIR")
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            _, img_encoded = cv2.imencode('.jpg', frame)
            img_bytes = img_encoded.tobytes()

            sio.emit('video_data', img_bytes)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except KeyboardInterrupt:
        pass
    finally:
        cap.release()
        sio.disconnect()




def send_audio():
    try:
        while True:
            data = input_stream.read(1024)
            sio.emit('audio_data', data)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except KeyboardInterrupt:
        pass
    finally:
        input_stream.stop_stream()
        input_stream.close()
        output_stream.stop_stream()
        output_stream.close()
        p.terminate()
        sio.disconnect()

@sio.event
def audio_data(data):
    output_stream.write(data)

if __name__ == '__main__':
     
    audioThread=threading.Thread(target=send_audio)
    videoThread=threading.Thread(target=send_video)
  
    #audioThread.start()
    #audioThread.join() 

    videoThread.start()
    #videoThread.join()
    #send_video()
    #send_audio()

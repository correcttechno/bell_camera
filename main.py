import threading
import cv2
from flask import Flask, Response, render_template, render_template_string
from client import sendVideo, setClientCameraFrame
from faceid import readFaceidFrame, setFaceIDCameraFrame


app = Flask(__name__)
cap = cv2.VideoCapture(0)

CAMERAFRAME=None


def read_camera():
    global CAMERAFRAME
    while True:
        ret,frame =cap.read()
        if not ret:
            break
        CAMERAFRAME=frame
        setClientCameraFrame(frame)
        setFaceIDCameraFrame(frame)


def generate_frames():
    global CAMERAFRAME
    while True:
        frame=CAMERAFRAME
        
        if CAMERAFRAME is None:
            break
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/bell',methods=['POST'])
def bell():
    return render_template_string("Salam")

if __name__ == '__main__':

    threading.Thread(target=read_camera).start()
    app.run(host='0.0.0.0', port=80, debug=False)


import threading
import time
import cv2
from flask import Flask, Response, render_template, render_template_string
from client import setClientCameraFrame
#from faceid import setFaceIDCameraFrame




app = Flask(__name__)
cap = cv2.VideoCapture('dev/video0')

#start face id and network
setClientCameraFrame(cap)
#setFaceIDCameraFrame(cap)

#generate http live
def generate_frames():
    while True:
        ret,frame=cap.read()
        if not ret:
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
    #sendText("BELL")
    return render_template_string("Salam")

if __name__ == '__main__':
    
    app.run(host='0.0.0.0', port=80, debug=False)


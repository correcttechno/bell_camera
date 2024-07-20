
import threading
import cv2
from flask import Flask, Response
from client import setClientCameraFrame
from faceid import setFaceIDCameraFrame



""" cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480) """

app = Flask(__name__)

def generate_frames():
    cam = cv2.VideoCapture(0)
    while True:
        # Frame'leri oku
        success, frame = cam.read()
        if not success:
            break
        setFaceIDCameraFrame(frame)    
        setClientCameraFrame(frame)    
        # Frame'i JPEG formatına çevir
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        
        # Frame'leri HTTP yanıtı olarak döndür
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    
   

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return """
    <html>
        <body>
            <h1>Webcam Video Feed</h1>
            <img src="/video_feed">
        </body>
    </html>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)


import threading
import cv2


from flask import Flask, Response
import cv2

#from client import setClientCameraFrame
from faceid import setFaceIDCameraFrame

cam = cv2.VideoCapture(0)

app = Flask(__name__)

def generate_frames():
    
    
    while True:
        # Frame'leri oku
        success, frame = cam.read()
        if not success:
            break
        setFaceIDCameraFrame(frame)    
        #setClientCameraFrame(frame)    
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

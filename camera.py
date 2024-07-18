import threading
import cv2

cam = cv2.VideoCapture("rtsp://admin:ruslan1424%@192.168.16.64:554/Streaming/Channels/101")

cleanFrame=None

def cameraCallback():
    global cleanFrame
    while True:
        ret,frame= cam.read()
        #frame=cv2.resize(frame,(320,240))
        cleanFrame=frame
        
            
    cam.release()

def readCameraFrame():
    global cleanFrame
    return cleanFrame

threading.Thread(target=cameraCallback).start()
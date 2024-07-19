import threading
import cv2

cam = cv2.VideoCapture(0)

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
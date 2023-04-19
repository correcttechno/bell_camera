import threading
import cv2

cam = cv2.VideoCapture(0)

cleanFrame=None

def cameraCallback():
    global cleanFrame
    while True:
        ret,frame= cam.read()
        
        cleanFrame=frame
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cam.release()

def readCameraFrame():
    global cleanFrame
    return cleanFrame

threading.Thread(target=cameraCallback).start()
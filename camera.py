import threading
import cv2

cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FPS, 30)

cleanFrame=None

def cameraCallback():
    global cleanFrame
    while True:
        ret,frame= cam.read()
        frame=cv2.resize(frame,(320,240))
        cleanFrame=frame
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cam.release()

def readCameraFrame():
    global cleanFrame
    return cleanFrame

threading.Thread(target=cameraCallback).start()
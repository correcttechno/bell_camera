import threading
import cv2

cam = cv2.VideoCapture(0)


def readCameraFrame():
    return cam.read()


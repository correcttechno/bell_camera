import cv2
import threading
import queue

# Kameradan veri alacak ana thread fonksiyonu
def camera_capture(shared_frame_queue):
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if ret:
            # En güncel çerçeveyi sıraya ekle
            if not shared_frame_queue.full():
                shared_frame_queue.put(frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()

# Thread'lerde görüntüyü işleyebilmek için bir sınıf
class FrameProcessor(threading.Thread):
    def __init__(self, shared_frame_queue, name):
        threading.Thread.__init__(self)
        self.shared_frame_queue = shared_frame_queue
        self.name = name

    def run(self):
        while True:
            if not self.shared_frame_queue.empty():
                frame = self.shared_frame_queue.get()
                # Burada her bir thread farklı işlem yapabilir, sadece gösterim yapalım
                cv2.imshow(self.name, frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

# Ana kamera verisini paylaşmak için bir sıra (queue) oluşturun
shared_frame_queue = queue.Queue(maxsize=1)

# Kameradan veri alan ana thread'i başlat
camera_thread = threading.Thread(target=camera_capture, args=(shared_frame_queue,))
camera_thread.start()

# İki farklı işlemci thread'i başlat (aynı kameradan gelen veriyi işleyebilirler)
processor1 = FrameProcessor(shared_frame_queue, "Processor 1")
processor2 = FrameProcessor(shared_frame_queue, "Processor 2")

processor1.start()
processor2.start()

camera_thread.join()
processor1.join()
processor2.join()
cv2.destroyAllWindows()

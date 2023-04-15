import cv2
import tkinter as tk
from PIL import Image, ImageTk

class VideoCapture:
    def __init__(self, video_source=1):
        self.cap = cv2.VideoCapture(video_source)
        if not self.cap.isOpened():
            raise ValueError("Unable to open video source", video_source)
        self.width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def __del__(self):
        if self.cap.isOpened():
            self.cap.release()

    def get_frame(self):
        if self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            else:
                return None
        else:
            return None

class App:
    def __init__(self, window, window_title, video_source=0):
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source

        # video source
        self.vid = VideoCapture(self.video_source)

        # canvas for displaying video
        self.canvas = tk.Canvas(window, width=self.vid.width, height=self.vid.height)
        self.canvas.pack()

        # button to capture video
        self.btn_snapshot = tk.Button(window, text="Snapshot", command=self.snapshot)
        self.btn_snapshot.pack(anchor=tk.CENTER, expand=True)

        # update the video display
        self.delay = 15
        self.update()

        self.window.mainloop()

    def snapshot(self):
        # get a frame from the video source
        frame = self.vid.get_frame()

        # convert to PIL image format
        image = Image.fromarray(frame)

        # save image
        image.save("snapshot.png")

    def update(self):
        # get a frame from the video source
        frame = self.vid.get_frame()

        if frame is not None:
            # convert to PIL image format
            image = Image.fromarray(frame)

            # show image on canvas
            self.photo = ImageTk.PhotoImage(image=image)
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        self.window.after(self.delay, self.update)

# create the app
App(tk.Tk(), "Tkinter Video Player")

import tkinter as tk
import cv2

class App:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)
        
        # pencereyi ikiye böl
        self.canvas = tk.Canvas(window, width=600, height=480)
        self.canvas.pack(side=tk.LEFT)
        
        # hesap makinesi widget'ını oluşturun
        self.calculator_frame = tk.Frame(window, bg="white", bd=5)
        self.calculator_frame.place(relx=0.7, rely=0.1, relwidth=0.25, relheight=0.8, anchor="n")
        self.label = tk.Label(self.calculator_frame, font=("Arial", 10), bg="white", anchor="e")
        self.label.place(relx=0, rely=0, relwidth=1, relheight=0.2)
        self.equation = ""
        
        # hesap makinesi butonlarını oluşturun
        buttons = ["C", "DEL", "/", "x",
                   "7", "8", "9", "-",
                   "4", "5", "6", "+",
                   "1", "2", "3", "=",
                   "0", ".", "(", ")"]
        x = 0
        y = 0
        for button in buttons:
            command = lambda x=button: self.button_click(x)
            tk.Button(self.calculator_frame, text=button, bg="white", fg="black", command=command).place(relx=x, rely=y, relwidth=0.25, relheight=0.2)
            x += 0.25
            if x >= 1:
                x = 0
                y += 0.2
        
        # video akışı widget'ını oluşturun
        self.video = cv2.VideoCapture(0)
        self.delay = 15 # milisaniye cinsinden
        self.update()
        self.window.mainloop()
    
    def button_click(self, key):
        if key == "C":
            self.equation = ""
        elif key == "DEL":
            self.equation = self.equation[:-1]
        elif key == "=":
            try:
                self.equation = str(eval(self.equation))
            except:
                self.equation = "Hata!"
        else:
            self.equation += str(key)
        self.label.config(text=self.equation)
        
    def update(self):
        ret, frame = self.video.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.photo = tk.PhotoImage(image=tk.BitmapImage(data=frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.window.after(self.delay, self.update)

App(tk.Tk(), "Hesap Makinesi ve Kamera Uygulaması")

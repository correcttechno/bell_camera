
import client
import threading
import tkinter as tk
import tkinter.font as tkFont
import cv2
from PIL import Image, ImageTk
from faceid import readFaceidFrame


root = tk.Tk()

""" bg_image = tk.PhotoImage(file="home/msb/bell_camera/backgroundimage.png")#"/home/msb/bell_camera/backgroundimage.png")
bg_label = tk.Label(root, image=bg_image)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)
 """





display=tk.Entry(root)
display["borderwidth"] = "1px"
ft = tkFont.Font(family='Roboto',size=30)
display["font"] = ft
display["fg"] = "#333333"
display["justify"] = "center"
display["text"] = "Entry"
display.place(x=670,y=40,width=259,height=60)


canvas = tk.Canvas(root)
canvas.place(x=70,y=100,width=500,height=400)
canvas.config(background="#000000",borderwidth=0)


#canvas.pack()

Button1=tk.Button(root)
Button1["bg"] = "#efefef"
ft = tkFont.Font(family='Roboto',size=28)
Button1["font"] = ft
Button1["fg"] = "#000000"
Button1["justify"] = "center"
Button1["text"] = "1"
Button1["relief"] = "sunken"
Button1.place(x=670,y=110,width=80,height=80)
Button1["command"] = lambda:ButtonClick('1')

Button2=tk.Button(root)
Button2["bg"] = "#efefef"
ft = tkFont.Font(family='Roboto',size=28)
Button2["font"] = ft
Button2["fg"] = "#000000"
Button2["justify"] = "center"
Button2["text"] = "2"
Button2.place(x=760,y=110,width=80,height=80)
Button2["command"] = lambda:ButtonClick(2)

Button3=tk.Button(root)
Button3["bg"] = "#efefef"
ft = tkFont.Font(family='Roboto',size=28)
Button3["font"] = ft
Button3["fg"] = "#000000"
Button3["justify"] = "center"
Button3["text"] = "3"
Button3.place(x=850,y=110,width=80,height=80)
Button3["command"] = lambda:ButtonClick(3)

Button4=tk.Button(root)
Button4["bg"] = "#efefef"
ft = tkFont.Font(family='Roboto',size=28)
Button4["font"] = ft
Button4["fg"] = "#000000"
Button4["justify"] = "center"
Button4["text"] = "4"
Button4.place(x=670,y=200,width=80,height=80)
Button4["command"] = lambda:ButtonClick(4)

Button5=tk.Button(root)
Button5["bg"] = "#efefef"
ft = tkFont.Font(family='Roboto',size=28)
Button5["font"] = ft
Button5["fg"] = "#000000"
Button5["justify"] = "center"
Button5["text"] = "5"
Button5.place(x=760,y=200,width=80,height=80)
Button5["command"] = lambda:ButtonClick(5)

Button6=tk.Button(root)
Button6["bg"] = "#efefef"
ft = tkFont.Font(family='Roboto',size=28)
Button6["font"] = ft
Button6["fg"] = "#000000"
Button6["justify"] = "center"
Button6["text"] = "6"
Button6.place(x=850,y=200,width=80,height=80)
Button6["command"] = lambda:ButtonClick(6)

Button7=tk.Button(root)
Button7["bg"] = "#efefef"
ft = tkFont.Font(family='Roboto',size=28)
Button7["font"] = ft
Button7["fg"] = "#000000"
Button7["justify"] = "center"
Button7["text"] = "7"
Button7.place(x=670,y=290,width=80,height=80)
Button7["command"] =lambda:ButtonClick(7)

Button8=tk.Button(root)
Button8["bg"] = "#efefef"
ft = tkFont.Font(family='Roboto',size=28)
Button8["font"] = ft
Button8["fg"] = "#000000"
Button8["justify"] = "center"
Button8["text"] = "8"
Button8.place(x=760,y=290,width=80,height=80)
Button8["command"] = lambda:ButtonClick(8)

Button9=tk.Button(root)
Button9["bg"] = "#efefef"
ft = tkFont.Font(family='Roboto',size=28)
Button9["font"] = ft
Button9["fg"] = "#000000"
Button9["justify"] = "center"
Button9["text"] = "9"
Button9.place(x=850,y=290,width=80,height=80)
Button9["command"] = lambda:ButtonClick(9)

GButton_184=tk.Button(root)
GButton_184["bg"] = "#efefef"
ft = tkFont.Font(family='Roboto',size=28)
GButton_184["font"] = ft
GButton_184["fg"] = "#000000"
GButton_184["justify"] = "center"
GButton_184["text"] = "*"
GButton_184.place(x=670,y=380,width=80,height=80)

GButton_735=tk.Button(root)
GButton_735["bg"] = "#efefef"
ft = tkFont.Font(family='Roboto',size=28)
GButton_735["font"] = ft
GButton_735["fg"] = "#000000"
GButton_735["justify"] = "center"
GButton_735["text"] = "0"
GButton_735.place(x=760,y=380,width=80,height=80)
GButton_735["command"] = lambda:ButtonClick(0)

GButton_690=tk.Button(root)
GButton_690["bg"] = "#efefef"
ft = tkFont.Font(family='Roboto',size=28)
GButton_690["font"] = ft
GButton_690["fg"] = "#000000"
GButton_690["justify"] = "center"
GButton_690["text"] = "#"
GButton_690.place(x=850,y=380,width=80,height=80)
 

GButton_339=tk.Button(root)
GButton_339["bg"] = "#5fb878"
ft = tkFont.Font(family='Roboto',size=18)
GButton_339["font"] = ft
GButton_339["fg"] = "#000000"
GButton_339["justify"] = "center"
GButton_339["text"] = "CALL"
GButton_339.place(x=670,y=470,width=260,height=49)

   

def ButtonClick(number):
    current = display.get()
    display.delete(0, tk.END)
    display.insert(0, str(current) + str(number))

   

def updateCam():
    while True:
        # Kamera görüntüsünü alma
        frame=readFaceidFrame()
        if frame is not None:
            frame=cv2.resize(frame,(500,400))
            # OpenCV görüntüsünü Tkinter için uygun formata dönüştürme
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            img_tk = ImageTk.PhotoImage(image=img)
            

            # Canvas'a görüntüyü ekleme
            canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)

            # Tkinter penceresini yenileme
            root.update()

cameraCam= threading.Thread(target=updateCam)
cameraCam.start()


#root.attributes("-fullscreen", True)

# Navigasyon çubuğunu gizle
root.overrideredirect(True)
root.configure(background="#000000")
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))



#root.after(10, show_frame)


#setting title
root.title("MSB Distant Door Bell")
#setting window size
width=1024
height=600
screenwidth = root.winfo_screenwidth()
screenheight = root.winfo_screenheight()
alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
root.geometry(alignstr)
root.resizable(width=False, height=False)

root.mainloop()
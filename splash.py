
import tkinter as tk

def splash():
    splash = tk.Toplevel()
    # Navigasyon çubuğunu gizle
    splash.overrideredirect(True)
    splash.configure(background="#7203FF")
    splash.geometry("{0}x{1}+0+0".format(splash.winfo_screenwidth(), splash.winfo_screenheight()))



    #root.after(10, show_frame)


    #setting title
    splash.title("MSB Distant")
    #setting window size
    width=1024
    height=600
    screenwidth = splash.winfo_screenwidth()
    screenheight = splash.winfo_screenheight()
    alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
    splash.geometry(alignstr)
    splash.resizable(width=False, height=False)
    
    splash.after(5000, splash.destroy)

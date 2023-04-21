
import tkinter as tk



root = tk.Tk()


# Navigasyon çubuğunu gizle
root.overrideredirect(True)
root.configure(background="#000000")
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))



#root.after(10, show_frame)


#setting title
root.title("MSB Distant")
#setting window size
width=1024
height=600
screenwidth = root.winfo_screenwidth()
screenheight = root.winfo_screenheight()
alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
root.geometry(alignstr)
root.resizable(width=False, height=False)

root.mainloop()
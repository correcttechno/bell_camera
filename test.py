import tkinter as tk

class Calculator:
    def __init__(self, master):
        self.master = master
        master.title("Hesap Makinesi")

        # Metin kutusu oluşturma
        self.display = tk.Entry(master, width=25, font=('Arial', 14))
        self.display.grid(row=0, column=0, columnspan=4, pady=5)

        # Rakam tuşlarını oluşturma
        self.button_1 = tk.Button(master, text="1", width=5, height=2, font=('Arial', 14),
                                  command=lambda: self.button_click('1'))
        self.button_2 = tk.Button(master, text="2", width=5, height=2, font=('Arial', 14),
                                  command=lambda: self.button_click('2'))
        self.button_3 = tk.Button(master, text="3", width=5, height=2, font=('Arial', 14),
                                  command=lambda: self.button_click('3'))
        self.button_4 = tk.Button(master, text="4", width=5, height=2, font=('Arial', 14),
                                  command=lambda: self.button_click('4'))
        self.button_5 = tk.Button(master, text="5", width=5, height=2, font=('Arial', 14),
                                  command=lambda: self.button_click('5'))
        self.button_6 = tk.Button(master, text="6", width=5, height=2, font=('Arial', 14),
                                  command=lambda: self.button_click('6'))
        self.button_7 = tk.Button(master, text="7", width=5, height=2, font=('Arial', 14),
                                  command=lambda: self.button_click('7'))
        self.button_8 = tk.Button(master, text="8", width=5, height=2, font=('Arial', 14),
                                  command=lambda: self.button_click('8'))
        self.button_9 = tk.Button(master, text="9", width=5, height=2, font=('Arial', 14),
                                  command=lambda: self.button_click('9'))
        self.button_0 = tk.Button(master, text="0", width=5, height=2, font=('Arial', 14),
                                  command=lambda: self.button_click('0'))

        # Operatör tuşlarını oluşturma
        self.button_add = tk.Button(master, text="+", width=5, height=2, font=('Arial', 14),
                                    command=lambda: self.button_click('+'))
        self.button_subtract = tk.Button(master, text="-", width=5, height=2, font=('Arial', 14),
                                         command=lambda: self.button_click('-'))
        self.button_multiply = tk.Button(master, text="*", width=5, height=2, font=('Arial', 14),
                                         command=lambda: self.button_click('*'))
        self.button_divide = tk.Button(master, text="/", width=5, height=2, font=('Arial', 14),
                                       command=lambda: self.button_click('/'))
        self.button_equal = tk.Button(master, text="=", width=5, height=2, font=('Arial', 14),
                                      command=self.calculate)
        self.button_clear = tk.Button(master, text="C", width=5, height=2, font=('Arial', 14),
                                      command=self.clear)

        # Tuşları düzenle
                # Tuşları düzenleme
        self.button_1.grid(row=3, column=0, padx=5, pady=5)
        self.button_2.grid(row=3, column=1, padx=5, pady=5)
        self.button_3.grid(row=3, column=2, padx=5, pady=5)
        self.button_4.grid(row=2, column=0, padx=5, pady=5)
        self.button_5.grid(row=2, column=1, padx=5, pady=5)
        self.button_6.grid(row=2, column=2, padx=5, pady=5)
        self.button_7.grid(row=1, column=0, padx=5, pady=5)
        self.button_8.grid(row=1, column=1, padx=5, pady=5)
        self.button_9.grid(row=1, column=2, padx=5, pady=5)
        self.button_0.grid(row=4, column=0, padx=5, pady=5)
        self.button_add.grid(row=1, column=3, padx=5, pady=5)
        self.button_subtract.grid(row=2, column=3, padx=5, pady=5)
        self.button_multiply.grid(row=3, column=3, padx=5, pady=5)
        self.button_divide.grid(row=4, column=3, padx=5, pady=5)
        self.button_equal.grid(row=4, column=2, padx=5, pady=5)
        self.button_clear.grid(row=4, column=1, padx=5, pady=5)

    def button_click(self, number):
        current = self.display.get()
        self.display.delete(0, tk.END)
        self.display.insert(0, str(current) + str(number))

    def clear(self):
        self.display.delete(0, tk.END)

    def calculate(self):
        result = eval(self.display.get())
        self.display.delete(0, tk.END)
        self.display.insert(0, result)


root = tk.Tk()
root.attributes("-fullscreen", True)

# Navigasyon çubuğunu gizle
root.overrideredirect(True)
root.configure(background="purple")
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))



calculator = Calculator(root)
root.mainloop()


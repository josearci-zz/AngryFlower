import sys
import tkinter as tk
from queue import Queue

class MainWindow(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master = master
        self.init_window()

    def init_window(self):
        tk.Label(self.master, text='%s, %s'%(1,2)).grid(row=1, column = 2)


if __name__== '__main__':
    root = tk.Tk()
    root.mainloop()

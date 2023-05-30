import tkinter as tk
from tkinter.ttk import *

class TopFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master=master, height=80, bg="red")
        self.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

class SideMenu(tk.Frame):
    def __init__(self, master):
        super().__init__(master=master, height=200,  width=200, bg="blue")
        self.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

class MainFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master=master, height=800, width=1200, bg="white")
        self.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

class MiddleFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master=master, height=1600)
        self.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

class Window:    
    def __init__(self):
        self.root = tk.Tk()
        self.top = TopFrame(self.root)
        self.middle = MiddleFrame(self.root)
        self.side = SideMenu(self.middle)
        self.main = MainFrame(self.middle)
        self.root.mainloop()

if __name__ == "__main__":
    window = Window()
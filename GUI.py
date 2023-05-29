import tkinter as tk
from tkinter.ttk import *

class TopFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master=master, height=200, bg="red")
        self.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

class SideMenu:
    def __init__(self, master):
        self.master = master

class MainFrame:
    def __init__(self, master):
        self.master = master

class Window:    
    def __init__(self):
        self.root = tk.Tk()
        self.top = TopFrame(self.root)
        self.side = SideMenu(self.root)
        self.main = MainFrame(self.root)
        self.root.mainloop()

if __name__ == "__main__":
    window = Window()
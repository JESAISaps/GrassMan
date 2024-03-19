import tkinter as tk
from tkinter import ttk

class MainApp():

    def __init__(self):
        self.root = tk.Tk()
        self.frame = ttk.Frame(self.root, padding=5)

        self.root.mainloop()

if __name__ == "__main__":
    MainApp()
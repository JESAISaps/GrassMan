import tkinter as tk
from tkinter import ttk, Tk

class MainApp(Tk):

    def __init__(self):

        super().__init__()
        
        self.geometry("720x420")

        self.exitButton = ttk.Button(self, text="Quitter", command=self.destroy)
        self.exitButton.pack(side="bottom")


if __name__ == "__main__":
    App = MainApp()
    App.mainloop()
import tkinter as tk
from tkinter import ttk, Tk, Button

class MainApp(Tk):

    def __init__(self):

        super().__init__()
        
        self.geometry("720x420")

        self.exitButton = Button(self, text="Quitter", command=self.destroy, bg="red")
        self.exitButton.pack(expand=1, fill="both")


if __name__ == "__main__":
    App = MainApp()
    App.mainloop()

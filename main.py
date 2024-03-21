import tkinter as tk
from tkinter import ttk, Tk

class MainApp(Tk):

    def __init__(self):

        #initializes Tk
        super().__init__()
        
        # sets window default size
        self.geometry("720x420")

        self.exitButton = tk.Button(self, text="Bouh", command=self.destroy, bg="red", font=("Helvetica", 40))
        self.exitButton.pack(expand=1, fill="both")


if __name__ == "__main__":
    App = MainApp()
    App.mainloop()

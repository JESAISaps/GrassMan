import tkinter as tk
from tkinter import ttk, Tk
#from ConvBDD import BDD
from matplotlib import pyplot as plt
from matplotlib import image as matim
import numpy as np
from PIL import Image, ImageTk

from stades import Stade
from scipy.ndimage import gaussian_filter

class App(tk.Tk):

    def __init__(self):

        #initializes Tk
        super().__init__()

        # creating a container
        self.container = tk.Frame(self)  
        self.container.pack(side = "top", fill = "both", expand = True)
        
        # sets default window size
        self.geometry("720x420")

        # initializing frames to an empty dict
        self.frames = {} # frames are the diferent pages you can open

        self.frames["HomeFrame"] = HomeFrame(self.container, self)
        self.frames["HomeFrame"].grid()
        self.frames["CreateStadium"] = CreateStadiumFrame(self.container, self)

        self.activeFrame = "HomeFrame"
        self.frames[self.activeFrame].tkraise()
        
    # to display the frame passed as parameter
    def show_frame(self, cont):

        self.frames[self.activeFrame].grid_forget()
        self.activeFrame = cont
        frame = self.frames[cont]
        frame.grid()
        frame.tkraise()

    def AddStadiumFrame(self, name, *dimensions):
        self.frames[name] = StadiumFrameTemplate(self.container, self, name, *dimensions)
        self.frames[name].grid()

class HomeFrame(tk.Frame):

    def __init__(self, parent:tk.Frame, controller:App):

        tk.Frame.__init__(self, parent)

        self.controller = controller

        self.createStadiumButton = ttk.Button(self, text="Creer un stade", command=lambda : self.controller.show_frame("CreateStadium"))
        self.createStadiumButton.pack()

class CreateStadiumFrame(tk.Frame):

    def __init__(self, parent:tk.Frame, controller:App):

        # initialises Frame
        tk.Frame.__init__(self, parent)

        self.controller = controller

        self.dimensionX = 100
        self.dimensionY = 50

        pageNameLabel = ttk.Label(self, text="Creation Stade")
        pageNameLabel.pack(side="top")

        self.stadiumNameLabel = ttk.Label(self, text="Nom du nouveau stade: ")
        self.stadiumNameLabel.pack()
        self.newStadiumNameEntry = ttk.Entry(self, textvariable="ex : Velodrome")
        self.newStadiumNameEntry.pack()
        self.newStadiumNameEntry.focus()

        self.dimensionEntryX = ttk.Entry(self, textvariable="X")
        self.dimensionEntryY = ttk.Entry(self, textvariable="Y")

        self.dimensionEntryX.pack(side="left")
        self.dimensionEntryY.pack(side="right")

        self.confirmButton = ttk.Button(self, text="Confirmer", command=self.CreateNewStadium)
        self.confirmButton.pack()

        self.ErrorLabel = ttk.Label(self, text = "Veuillez verifier vos entrées")
    
    def CreateNewStadium(self):
        if self.CheckValues():
            self.controller.AddStadiumFrame(self.newStadiumNameEntry.get(), int(self.dimensionEntryX.get()), int(self.dimensionEntryY.get()))
            self.controller.show_frame(self.newStadiumNameEntry.get())
        else:
            self.ErrorLabel.pack(side="bottom")
    
    def CheckValues(self):
        isGood = True
        if self.newStadiumNameEntry.get().replace(" ", "") == "":
            isGood = False
            self.newStadiumNameEntry.delete(0, "end")
        try:
            self.dimensionX = int(self.dimensionEntryX.get())
            self.dimensionY = int(self.dimensionEntryY.get())
        except:
            isGood = False
            self.dimensionEntryX.delete(0, 'end')
            self.dimensionEntryY.delete(0, 'end')
        return isGood
    
class StadiumFrameTemplate(tk.Frame):

    def __init__(self, parent:tk.Frame, controller:App, nomStade:str, *dimentions):

        # initialises Frame
        tk.Frame.__init__(self, parent)

        self.name = nomStade

        #create the stadium we'll get data from
        self.stade = Stade(nomStade, *dimentions)
        
        
        self.graphImage = self.createGraph(self.stade.getTemp())
        self.graphLabel = tk.Label(self, image=self.graphImage)
        self.graphLabel.pack(side="left")

        self.refreshGraphButton = tk.Button(self, text="Refresh", command=self.updateGraph, font=("Helvetica", 25))
        self.refreshGraphButton.pack(side="right", padx=30, pady=30)


    def createGraph(self, data):
        imageData = np.array(gaussian_filter([[[0,0,(element+20)*7] for element in ligne] for ligne in data], sigma=0.75)).astype(np.uint8)

        matim.imsave("./temp.gitignore/tempGraph.png", imageData)
        image = Image.open("./temp.gitignore/tempGraph.png")

        image = image.resize((500, 250))

        photo = ImageTk.PhotoImage(image)

        return photo

    def updateGraph(self):
        # On detruit l'objet du graphe pour le recreer
        self.graphLabel.destroy()

        #on met a jour les données de temperature
        self.stade.modifTemp()

        #on recrée le graphe
        self.graphImage = self.createGraph(self.stade.getTemp())        
        self.graphLabel = tk.Label(self, image=self.graphImage)  
        self.graphLabel.pack(side="left")

if __name__ == "__main__":

    #App = StadiumFrameTemplate("Velodrome", 100, 50)
    #App.mainloop()

    palala = App()
    palala.mainloop()

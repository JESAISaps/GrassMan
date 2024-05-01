import tkinter as tk
from tkinter import ttk, Tk
#from ConvBDD import BDD
from matplotlib import pyplot as plt
from matplotlib import image as matim
import numpy as np
from PIL import Image, ImageTk

from stades import Stade
from scipy.ndimage import gaussian_filter

class App(Tk):

    def __init__(self):

        #initializes Tk
        super().__init__()

        # creating a container
        self.container = tk.Frame(self)
        self.container.pack(side = "top", fill = "both", expand = True)
        
        # sets default window size
        self.geometry("720x420")
        self.resizable = False

        # initializing frames to an empty dict
        self.frames = {} # frames are the diferent pages you can open

        self.frames["HomeFrame"] = HomeFrame(self.container, self)
        self.frames["HomeFrame"].grid(sticky="nswe")
        self.frames["CreateStadium"] = CreateStadiumFrame(self.container, self)

        self.activeFrame = "HomeFrame"
        self.frames[self.activeFrame].tkraise()
        
    # to display the frame passed as parameter
    def show_frame(self, cont):

        # remove current page
        self.frames[self.activeFrame].grid_forget()

        # sets up new frame
        self.activeFrame = cont
        frame = self.frames[cont]
        frame.grid(sticky="nswe")
        frame.tkraise()

    def AddStadiumFrame(self, name, *dimensions):
        self.frames[name] = StadiumFrameTemplate(self.container, self, name, *dimensions)
        self.frames[name].grid(sticky="nswe")

class HomeFrame(tk.Frame):

    def __init__(self, parent:tk.Frame, controller:App):

        tk.Frame.__init__(self, parent, highlightbackground="black", highlightthickness=1)
        self.grid_rowconfigure(1)
        self.grid_rowconfigure(2)
        self.grid_rowconfigure(3)
        self.grid_rowconfigure(4)
        self.grid_rowconfigure(5)
        self.grid_rowconfigure(6)
        self.grid_rowconfigure(7)
        self.grid_rowconfigure(8)
        self.grid_rowconfigure(9)

        self.grid_culumnconfigure(1)
        self.grid_culumnconfigure(1)
        self.grid_culumnconfigure(1)
        self.grid_culumnconfigure(1)
        self.grid_culumnconfigure(1)
        self.grid_culumnconfigure(1)
        self.grid_culumnconfigure(1)
        self.grid_culumnconfigure(1)
        self.grid_culumnconfigure(1)

        print(self.grid_size())
        # reference to controller main window, might be usefull
        self.controller = controller        

        self.userId = tk.StringVar
        self.idInput = ttk.Entry(self, textvariable=self.userId)
        self.idInputLabel = ttk.Label(self, text="Identifiant :")

        self.idInputLabel.grid(column=50)
        self.idInput.grid()

        #self.createStadiumButton = ttk.Button(self, text="Creer un stade", command=lambda : self.controller.show_frame("CreateStadium"))
        #self.createStadiumButton.grid(row=5, column=2, columnspan=3)

class CreateStadiumFrame(tk.Frame):

    def __init__(self, parent:tk.Frame, controller:App):

        # initialises Frame
        tk.Frame.__init__(self, parent)

        self.controller = controller

        # default dimensions, will not be used, it's just for initialisation
        self.dimensionX = 100
        self.dimensionY = 50

        pageNameLabel = ttk.Label(self, text="Creation Stade")
        pageNameLabel.pack(side="top")

        self.stadiumNameLabel = ttk.Label(self, text="Nom du nouveau stade: ")
        self.stadiumNameLabel.pack()

        self.stadiumName = tk.StringVar()
        self.newStadiumNameEntry = ttk.Entry(self, textvariable=self.stadiumName)
        self.newStadiumNameEntry.pack()
        self.newStadiumNameEntry.focus()

        self.xDim = tk.StringVar()
        self.yDim = tk.StringVar()
        self.dimensionEntryX = ttk.Entry(self, textvariable=self.xDim)
        self.dimensionEntryY = ttk.Entry(self, textvariable=self.yDim)

        self.dimensionEntryX.pack(side="left")
        self.dimensionEntryY.pack(side="right")

        self.confirmButton = ttk.Button(self, text="Confirmer", command=self.CreateNewStadium)
        self.confirmButton.pack()

        self.ErrorLabel = ttk.Label(self, text = "Veuillez verifier vos entrées")
    
    def CreateNewStadium(self):
        """
        Calls funtion to check in inputs are correct and calls App method to add the stadium
        """
        if self.CheckValues():
            self.controller.AddStadiumFrame(self.stadiumName.get(), int(self.xDim.get()), int(self.yDim.get()))
            self.controller.show_frame(self.stadiumName.get())
        else:
            self.ErrorLabel.pack(side="bottom")
    
    def CheckValues(self):
        isGood = True

        # name must not be empty or just spaces
        if self.stadiumName.get().replace(" ", "") == "":
            isGood = False
            self.newStadiumNameEntry.delete(0, "end")
        try:
            # dimensions must not be empty or NaN
            self.dimensionX = int(self.xDim.get())
            self.dimensionY = int(self.xDim.get())
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
        """
        returns image to show
        """
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

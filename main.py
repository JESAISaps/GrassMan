import tkinter as tk
from tkinter import ttk, Tk
from ConvBDD import BDD
from matplotlib import pyplot as plt
from matplotlib import image as matim
import numpy as np
from PIL import Image, ImageTk

from stades import Stade
from scipy.ndimage import gaussian_filter


class MainApp(Tk):

    def __init__(self):

        #initializes Tk
        super().__init__()

        self.stade = Stade("Velodrome")
        
        # sets window default size
        self.geometry("720x420")

        #self.exitButton = tk.Button(self, text="Bouh", command=self.destroy, bg="red", font=("Helvetica", 40))
        #self.exitButton.pack(side="right")
        
        self.graphImage = self.createGraph(self.stade.getTemp())
        self.graphLabel = tk.Label(self, image=self.graphImage)
        self.graphLabel.pack(side="left")

        self.refreshGraphButton = tk.Button(self, text="Refresh", command=self.updateGraph, font=("Helvetica", 25))
        self.refreshGraphButton.pack(side="right", padx=30, pady=30)


    def createGraph(self, data):
        imageData = np.array(gaussian_filter([[[0,0,(element+20)*7] for element in ligne] for ligne in data], sigma=0.75)).astype(np.uint8)
        #self.imageData = np.array([[[0,0,(element+20)*7] for element in ligne] for ligne in stade.getTemp()]).astype(np.uint8)

        matim.imsave("./temp.gitignore/tempGraph.png", imageData)
        image = Image.open("./temp.gitignore/tempGraph.png")

        image = image.resize((500, 250))

        photo = ImageTk.PhotoImage(image)

        return photo

    def updateGraph(self):
        # On detruit l'objet du graph pour le recreer
        self.graphLabel.destroy()

        #on met a jour les données de temperatures
        self.stade.modifTemp()

        #on recrée le graph
        self.graphImage = self.createGraph(self.stade.getTemp())        
        self.graphLabel = tk.Label(self, image=self.graphImage)  
        self.graphLabel.pack(side="left")

if __name__ == "__main__":
    App = MainApp()
    App.mainloop()
    #plt.imshow(gaussian_filter([[[0,0,(element+20)*7] for element in ligne] for ligne in Stade("Blob").getTemp()], sigma=1.5))
    #plt.show()

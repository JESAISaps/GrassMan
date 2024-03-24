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
        self.showTemps(self.stade)

    #def createTempGraph(self, stade:Stade):
    #    tempsImage = plt.imshow([[[0,0,(element+20)*7] for element in ligne] for ligne in stade.getTemp()])
    #    tempsImage = gaussian_filter(tempsImage, sigma=1.5)
    #    return tempsImage
    
    def showTemps(self, stade:Stade):

        self.imageData = np.array(gaussian_filter([[[0,0,(element+20)*7] for element in ligne] for ligne in stade.getTemp()], sigma=0.75)).astype(np.uint8)

        matim.imsave("./temp/tempTemp.png", self.imageData)
        self.image = Image.open("./temp/tempTemp.png")

        self.image = self.image.resize((500, 250))

        self.photo = ImageTk.PhotoImage(self.image)

        label = tk.Label(self, image=self.photo)
        label.pack(expand=1, side="left",fill="both")



if __name__ == "__main__":
    App = MainApp()
    App.mainloop()
    #plt.imshow(gaussian_filter([[[0,0,(element+20)*7] for element in ligne] for ligne in Stade("Blob").getTemp()], sigma=1.5))
    #plt.show()

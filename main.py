import tkinter as tk
from tkinter import ttk, Tk
#from ConvBDD import BDD
from matplotlib import pyplot as plt
from matplotlib import image as matim
import numpy as np
from PIL import Image, ImageTk
import motdepasse

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
        self.frames["HomeFrame"].pack(expand=True)
        self.frames["CreateStadium"] = CreateStadiumFrame(self.container, self)

        self.activeFrame = "HomeFrame"
        self.frames[self.activeFrame].tkraise()
        
    # to display the frame passed as parameter
    def show_frame(self, cont):

        # remove current page
        self.frames[self.activeFrame].pack_forget()

        # sets up new frame
        self.activeFrame = cont
        frame = self.frames[cont]
        frame.pack(expand=True)
        frame.tkraise()

    def AddStadiumFrame(self, name, *dimensions):
        self.frames[name] = StadiumFrameTemplate(self.container, self, name, *dimensions)
        self.frames[name].pack(expand=True)

class SideMenu(tk.Frame):

    def __init__(self, parent, root):
        self.root = root
        self.min_w = 50 # Minimum width of the frame
        self.max_w = 180 # Maximum width of the frame
        self.cur_width = self.min_w # Increasing width of the frame
        self.expanded = False # Check if it is completely exanded

        # Define the icons to be shown and resize it
        #self.home = ImageTk.PhotoImage(Image.open('home.png').resize((40,40)))
        #self.settings = ImageTk.PhotoImage(Image.open('settings.png').resize((40,40)))
        #self.ring = ImageTk.PhotoImage(Image.open('ring.png').resize((40,40)))   

        self.root.update() # For the width to get updated

        tk.Frame.__init__(self, parent, bg='#32cd32',width=50,height=root.winfo_height())
        self.pack(side="right", fill=tk.Y)

        self.passwordLabel = tk.Label(self, text="Mot de passe")
        # Creates the entries along with labels
        self.password1, self.password2 = tk.StringVar(), tk.StringVar()
        self.passwordEntry1 = ttk.Entry(self, textvariable=self.password1)

        self.passwordLabel2 = tk.Label(self, text="Repetez le mot de passe")
        self.passwordEntry2 = ttk.Entry(self, textvariable=self.password2)

        self.passwordLabel.pack()
        self.passwordEntry1.pack()
        self.passwordLabel2.pack()
        self.passwordEntry2.pack()

        # Make the buttons with the icons to be shown
        #self.home_b = tk.Button(self,image=self.home,bg='#32cd32',relief='flat', activebackground='#349834')
        #self.set_b = tk.Button(self, image=self.settings,bg='#32cd32',relief='flat', activebackground='#349834')
        #self.ring_b = tk.Button(self,image=self.ring,bg='#32cd32',relief='flat', activebackground='#349834')

        #self.home_b.pack(pady=10)
        #self.set_b.pack(pady=50)
        #self.ring_b.pack()

        # Bind to the frame, if entered or left
        self.bind('<Enter>',lambda e: self.expand())
        self.bind('<Leave>',lambda e: self.contract())  

        # So that it does not depend on the widgets inside the frame
        self.pack_propagate(False)
    
    def expand(self):
        self.cur_width += 10 # Increase the width by 10
        self.rep = self.root.after(5,self.expand) # Repeat this func every 5 ms
        self.config(width=self.cur_width) # Change the width to new increase width
        if self.cur_width >= self.max_w: # If width is greater than maximum width 
            self.expanded = True # Frame is expended
            self.root.after_cancel(self.rep) # Stop repeating the func
            self.fill()

    def contract(self):
        self.cur_width -= 10 # Reduce the width by 10 
        self.rep = self.root.after(5,self.contract) # Call this func every 5 ms
        self.config(width=self.cur_width) # Change the width to new reduced width
        if self.cur_width <= self.min_w: # If it is back to normal width
            self.expanded = False # Frame is not expanded
            self.root.after_cancel(self.rep) # Stop repeating the func
            self.fill()
    
    def fill(self):
        if self.expanded: # If the frame is s
            return
            # Show a text, and remove the image
            self.home_b.config(text='Home',image='',font=(0,21))
            self.set_b.config(text='Settings',image='',font=(0,21))
            self.ring_b.config(text='Bell Icon',image='',font=(0,21))
        else:
            return
            # Bring the image back
            self.home_b.config(image=self.home,font=(0,21))
            self.set_b.config(image=self.settings,font=(0,21))
            self.ring_b.config(image=self.ring,font=(0,21))
    
    

class HomeFrame(tk.Frame):

    def __init__(self, parent:tk.Frame, controller:App):

        tk.Frame.__init__(self, parent)
        # reference to controller main window, might be usefulls
        self.controller = controller
        self.parent = parent

        self.userId = tk.StringVar
        self.idInput = ttk.Entry(self, textvariable=self.userId)
        self.idInputLabel = ttk.Label(self, text="Identifiant :")

        self.password = tk.StringVar
        self.passwordInput = ttk.Entry(self, textvariable=self.password, show="*")
        self.passwordInputLabel = ttk.Label(self, text="Mot de passe :")

        self.idInputLabel.pack(side="top")
        self.idInput.pack(side="top")

        self.passwordInputLabel.pack(side="top",ipady=10)
        self.passwordInput.pack(side="top")

        self.confirmButton = ttk.Button(self, text="Confirmer", command= lambda : self.CheckLogin(self.userId, self.password))
        self.confirmButton.pack(side="bottom")

        self.SideMenu = SideMenu(parent, self)        

    def CheckLogin(self, id, psw):
        if motdepasse.connection(id, psw):
            print("Acces autorise")
            #TODO: connecter lutilisateur
            return
        else:
            print("Hehe non")
            return


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

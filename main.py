import tkinter as tk
from tkinter import ttk, Tk
#from ConvBDD import BDD
from matplotlib import pyplot as plt
from matplotlib import image as matim
import numpy as np
from PIL import Image, ImageTk
import BDDapi
import sqlite3
from tkscrolledframe import ScrolledFrame

from stades import Stade
from scipy.ndimage import gaussian_filter

class App(Tk):

    def __init__(self):

        self.BDDPATH = "./data/bddstade.db"
        self.client = None

        #initializes Tk
        super().__init__()

        # creating a container
        self.container = tk.Frame(self)
        self.container.pack(side = "top", fill = "both", expand = True)
        
        # sets default window size
        self.geometry("720x420")
        self.resizable(False, False)

        # initializing frames to an empty dict
        self.frames = {} # frames are the diferent pages you can open

        self.frames["HomeFrame"] = HomeFrame(self.container, self)
        self.frames["HomeFrame"].pack(expand=True)
        self.frames["CreateStadium"] = CreateStadiumFrame(self.container, self)
        self.frames["StadiumList"] = StadiumListFrame(self.container, self)

        self.activeFrame = "HomeFrame"
        self.frames[self.activeFrame].tkraise()

        
    # to display the frame passed as parameter
    def show_frame(self, cont:str):

        # remove current page
        self.frames[self.activeFrame].pack_forget()

        # sets up new frame
        self.activeFrame = cont
        frame = self.frames[cont]
        frame.pack(expand=True)
        frame.tkraise()

    def AddStadiumFrame(self, name, dimensions=(100, 50)):
        if name in ["HomeFrame", "CreateStadium", "Stadiumlist"]:
            print("Nom de stade reservé")
            return

        self.frames[name] = StadiumFrameTemplate(self.container, self, name, dimensions)
        #self.frames[name].pack(expand=True)

    def createUserSession(self, id):
        if self.client is not None:
            print("Error, existing session running")
            return
        else:
            self.client = User(self, id)    
    
    def CreateStadiumFrames(self):

        stadiumList = self.client.GetClientStadiums()
        for stadium in stadiumList:
            self.AddStadiumFrame(stadium)


class User:

    def __init__(self, root:App, id=None):
        self.root = root
        self.id = id
        self.stadiumList = self.RefreshClientStadiums()
        
    def GetClientId(self)->str:
        return self.id
    
    def GetClientStadiums(self)->list[str]:
        return self.stadiumList
    
    def RefreshClientStadiums(self)->list[str]:

        bdd = sqlite3.connect(self.root.BDDPATH)
        rep = BDDapi.GetClientStadiums(bdd, self.root.client)
        self.stadiumList = rep
        bdd.close()
        return rep
    

class SideMenu(tk.Frame):

    def __init__(self, parent, root:App):
        self.root = root
        self.min_w = 50 # Minimum width of the frame
        self.max_w = 180 # Maximum width of the frame
        self.cur_width = self.min_w # Increasing width of the frame
        self.expanded = False # Check if it is completely exanded
        self.isMoving = False # So we dont interupt the window resizement
        self.hasChanged = False

        # Define the icon to be shown and resize it
        self.plusImage = ImageTk.PhotoImage(Image.open("./data/images/plus.png").resize((40, 40)))

        self.root.update() # For the width to get updated

        tk.Frame.__init__(self, parent, bg='#32cd32',width=50,height=root.winfo_height())
        self.pack(side="right", fill=tk.Y)

        self.nameLabel = ttk.Label(self, text="Entrez votre prenom", background="#32cd32")
        self.name = tk.StringVar()
        self.nameEntry = ttk.Entry(self, textvariable=self.name)

        self.name2Label = ttk.Label(self, text="Entrez votre nom : ", background="#32cd32")
        self.name2 = tk.StringVar()
        self.name2Entry = ttk.Entry(self, textvariable=self.name2)

        self.idLabel = ttk.Label(self, text="Créez un identifiant : ", background="#32cd32")
        self.id = tk.StringVar()
        self.idEntry = ttk.Entry(self, textvariable=self.id)

        self.passwordLabel1 = ttk.Label(self, text="Créez un mot de passe", background='#32cd32')
        # Creates the entries along with labels
        self.password1, self.password2 = tk.StringVar(), tk.StringVar()
        self.passwordEntry1 = ttk.Entry(self, textvariable=self.password1, show="•")

        self.passwordLabel2 = ttk.Label(self, text="Confirmez le mot de passe", background='#32cd32')
        self.passwordEntry2 = ttk.Entry(self, textvariable=self.password2, show="•")

        self.isLocked = tk.BooleanVar()
        self.lockMenuButton = ttk.Checkbutton(self, variable=self.isLocked, text="Bloquer le menu")

        self.confirmButton = ttk.Button(self, text="Créer", command=lambda : self.CreateUser(self.id.get(), self.password1.get(), self.password2.get(), self.name.get(), self.name2.get()))

        self.plusImageObject = tk.Label(self, image=self.plusImage, bg="#32cd32")


        self.plusImageObject.pack(fill="none", expand=True)

        # Bind to the frame, if entered or left
        self.bind('<Enter>',lambda e: self.expand() if self.isMoving is False else SetHasChanged())
        self.bind('<Leave>',lambda e: self.contract() if self.isMoving is False else SetHasChanged())

        def SetHasChanged():
            """
            Fix for menu not retracting if user is too fast
            """
            self.hasChanged = not self.hasChanged

        # So that it does not depend on the widgets inside the frame
        self.pack_propagate(False)
    
    def expand(self)->None:
        if(self.expanded):
            return
        self.isMoving = True
        self.cur_width += 15 # Increase the width by 15
        self.rep = self.root.after(5,self.expand) # Repeat this func every 5 ms
        self.config(width=self.cur_width) # Change the width to new increase width
        if self.cur_width >= self.max_w: # If width is greater than maximum width 
            self.expanded = True # Frame is expended
            self.root.after_cancel(self.rep) # Stop repeating the func
            self.isMoving = False

            if self.hasChanged:
                self.hasChanged = False
                self.contract()
            self.fill()

    def contract(self)->None:
        if(self.isLocked.get()):
            return
        self.isMoving = False
        self.cur_width -= 15 # Reduce the width by 15
        self.rep = self.root.after(5,self.contract) # Call this func every 5 ms
        self.config(width=self.cur_width) # Change the width to new reduced width
        if self.cur_width <= self.min_w: # If it is back to normal width
            self.expanded = False # Frame is not expanded
            self.root.after_cancel(self.rep) # Stop repeating the func
            self.cur_width = self.min_w # if we went too far
            self.isMoving = False

            if self.hasChanged:
                self.hasChanged = False
                self.expand()
            self.fill()
    
    def fill(self)->None:
        if self.expanded: # If the frame is extended

            # Show everything, hide image
            self.plusImageObject.pack_forget()

            self.nameLabel.pack(side="top", pady=(20, 0))
            self.nameEntry.pack(side="top", pady=(0, 10))

            self.name2Label.pack(side="top", pady=(5, 0))
            self.name2Entry.pack(side="top", pady=(0, 10))

            self.idLabel.pack(side="top", pady=(10, 0))
            self.idEntry.pack(side="top", pady=(0, 25))

            self.passwordLabel1.pack(pady=(30, 0))
            self.passwordEntry1.pack(pady=(0, 20))

            self.passwordLabel2.pack()
            self.passwordEntry2.pack()

            self.lockMenuButton.pack()
            self.confirmButton.pack(side="bottom")
        else:
            # hide everything
            self.nameLabel.pack_forget()
            self.nameEntry.pack_forget()

            self.name2Label.pack_forget()
            self.name2Entry.pack_forget()

            self.idLabel.pack_forget()
            self.idEntry.pack_forget()

            self.passwordLabel1.pack_forget()
            self.passwordEntry1.pack_forget()

            self.passwordLabel2.pack_forget()
            self.passwordEntry2.pack_forget()

            self.lockMenuButton.pack_forget()
            self.confirmButton.pack_forget()

            # Bring the image back
            self.plusImageObject.pack(fill="none", expand=True)

    def MismachPassword(self)->None:
        self.passwordMismachErrorLabel = ttk.Label(self, text="Erreur dans la confirmation du \nmot de passe", background="red", justify="center")
        self.passwordMismachErrorLabel.pack(side="bottom", pady=(0, 2))
        self.after(2000, self.passwordMismachErrorLabel.destroy)

    def DuplacateId(self)->None:
        self.duplicateIdLabel = ttk.Label(self, text="Ce nom d'utilisateur existe déjà !", background="red", justify="center")
        self.duplicateIdLabel.pack(side="bottom", pady=(0, 2))        
        self.after(2000, self.duplicateIdLabel.destroy)

    def UserCreated(self)->None:
        self.UserCreatedLabel = ttk.Label(self, text="Utilisateur créé avec succes,\nvous pouvez vous connecter.", background="green", justify="center")
        self.UserCreatedLabel.pack(side="bottom", pady=(0, 2))
        self.after(2000, self.UserCreatedLabel.destroy)
    
    def CreateUser(self, id, psw1, psw2, name, name2)->None:        
        bdd = sqlite3.connect(self.root.BDDPATH)
        if psw1 != psw2:
            self.MismachPassword()
        elif BDDapi.CheckIfIdExists(bdd, self.id.get()):
            self.DuplacateId()
        else:        
            BDDapi.nouveauclient(bdd, id, name2, name, psw1)
            bdd.commit()
            self.UserCreated()
        bdd.close()
        

class HomeFrame(tk.Frame):

    def __init__(self, parent:tk.Frame, root:App):

        tk.Frame.__init__(self, parent)
        # reference to controller main window, might be usefulls
        self.root = root
        self.parent = parent
        self.userId = tk.StringVar()
        self.idInput = ttk.Entry(self, textvariable=self.userId)
        self.idInputLabel = ttk.Label(self, text="Identifiant :")

        self.password = tk.StringVar()
        self.passwordInput = ttk.Entry(self, textvariable=self.password, show="•")
        self.passwordInputLabel = ttk.Label(self, text="Mot de passe :")

        self.idInputLabel.pack(side="top")
        self.idInput.pack(side="top")

        self.passwordInputLabel.pack(side="top",ipady=10)
        self.passwordInput.pack(side="top")

        self.confirmButton = ttk.Button(self, text="Confirmer", command= lambda : self.LoginUser(self.userId.get(), self.password.get()))
        self.confirmButton.pack(side="bottom")

        self.SideMenu = SideMenu(parent, self.root)        

    def LoginUser(self, id, psw)->None:
        bdd = sqlite3.connect(self.root.BDDPATH)
        access = BDDapi.connection(bdd, id, psw)
        bdd.close()
        #pour test des menus
        if id == "azerty":
            self.root.show_frame("StadiumList")
            return

        if access:
            print("Acces autorise")
            #TODO: connecter l'utilisateur
            self.root.createUserSession(id)
            self.root.CreateStadiumFrames()
            self.root.show_frame("StadiumList")
            self.root.frames["StadiumList"].ShowButtons()
            return
        else:
            print("Hehe non")
            return


class CreateStadiumFrame(tk.Frame):

    def __init__(self, parent:tk.Frame, root:App):

        # initialises Frame
        tk.Frame.__init__(self, parent)

        self.controller = root

        # default values, will not be used, it's just for initialisation
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
    
    def CreateNewStadium(self)->None:
        """
        Calls funtion to check in inputs are correct and calls App method to add the stadium
        """
        if self.CheckValues():
            self.controller.AddStadiumFrame(self.stadiumName.get(), (int(self.xDim.get()), int(self.yDim.get())))
            self.controller.show_frame(self.stadiumName.get())
        else:
            self.ErrorLabel.pack(side="bottom")
    
    def CheckValues(self)->bool:
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

    def __init__(self, parent:tk.Frame, root:App, nomStade:str, dimentions):

        # initialises Frame
        tk.Frame.__init__(self, parent)

        self.name = nomStade

        #create the stadium we'll get data from
        self.stade = Stade(nomStade, dimentions, "hiver")
        
        
        self.graphImage = self.createGraph(self.stade.getTemp())
        self.graphLabel = tk.Label(self, image=self.graphImage)
        self.graphLabel.pack(side="left")

        self.refreshGraphButton = tk.Button(self, text="Refresh", command=self.updateGraph, font=("Helvetica", 25))
        self.refreshGraphButton.pack(side="right", padx=30, pady=30)


    def createGraph(self, data)->Image:
        """
        returns image to show
        """
        imageData = np.array(gaussian_filter([[[0,0,(element+20)*7] for element in ligne] for ligne in data], sigma=0.75)).astype(np.uint8)

        matim.imsave("./temp/tempGraph.png", imageData)
        image = Image.open("./temp/tempGraph.png")

        image = image.resize((500, 250))

        photo = ImageTk.PhotoImage(image)

        return photo

    def updateGraph(self)->None:
        # On detruit l'objet du graphe pour le recreer
        self.graphLabel.destroy()

        #on met a jour les données de temperature
        self.stade.modifTemp()

        #on recrée le graphe
        self.graphImage = self.createGraph(self.stade.getTemp())        
        self.graphLabel = tk.Label(self, image=self.graphImage)  
        self.graphLabel.pack(side="left")

class StadiumListFrame(tk.Frame):

    def __init__(self, parent:tk.Frame, root:App):
        
        tk.Frame.__init__(self, parent)
        self.root = root
        self.parent = parent
        self.list = ScrolledFrame(self, width = 400, height = 200, scrollbars = "vertical", use_ttk = True)
        self.list.pack(side="left")
        self.displayWidget = self.list.display_widget(tk.Frame)

        self.createStadiumBUtton = ttk.Button(self, text="Creer un nouveau stade", command=lambda : root.show_frame("CreateStadium"))
        self.createStadiumBUtton.pack(side="right")

    def ShowButtons(self)->None:
        self.stadiumsToShow = self.root.client.GetClientStadiums()
        print(self.stadiumsToShow)
        for stadium in self.stadiumsToShow:
            button = ttk.Button(self.displayWidget, text=stadium, command= lambda : self.root.show_frame(stadium))
            button.pack()
        #self.root.update_idletasks()

        
if __name__ == "__main__":

    #App = StadiumFrameTemplate("Velodrome", 100, 50)
    #App.mainloop()

    palala = App()
    palala.mainloop()

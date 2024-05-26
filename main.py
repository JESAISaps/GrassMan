import tkinter as tk
from tkinter import ttk, Tk
import numpy as np
from PIL import Image, ImageTk
import BDDapi
import Graphs
import sqlite3
from tkscrolledframe import ScrolledFrame
import tkcalendar
from datetime import datetime, timedelta
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from stades import Stade
from scipy.ndimage import gaussian_filter

# Global var, for colors:
GREEN = "#32cd32"
GREY = "#D3D3D3"

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
        self.geometry("1080x720")
        self.resizable(False, False)

        # initializing frames to an empty dict
        self.frames:dict[tk.Frame] = {} # frames are the different pages you can open

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
        frame.pack_propagate(False)
        frame.pack(expand=True)
        frame.tkraise()

    def AddStadiumFrame(self, name, dimensions=(100, 50)):
        if name in ["HomeFrame", "CreateStadium", "StadiumList"]:
            print("Nom de stade reservé")
            return

        self.frames[name] = StadiumFrameTemplate(self.container, self, name, dimensions)

    def createUserSession(self, id):
        if self.client is not None:
            print("Error, existing session running")
            return
        else:
            self.client = Client(self, id)    
    
    def CreateStadiumFrames(self):

        stadiumList = self.client.GetClientStadiums()
        #print(stadiumList)
        for stadium in stadiumList:
            self.AddStadiumFrame(stadium)

    def DisconnectClient(self):
        self.show_frame("HomeFrame")
        self.client = None
        temp = self.frames.copy()
        for stadiumName in temp:
            if stadiumName not in ["HomeFrame", "CreateStadium", "StadiumList"]:
                self.frames.pop(stadiumName)


class Client:

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
        rep = BDDapi.GetClientStadiums(bdd, self.id)
        self.stadiumList = rep
        bdd.close()
        return rep


class SideMenu(tk.Frame):

    def __init__(self, parent, root:App):
        self.root = root
        self.root.update_idletasks()
        self.min_w = self.root.winfo_width()//15 # Minimum width of the frame
        self.max_w = self.root.winfo_width()//5 # Maximum width of the frame
        self.cur_width = self.min_w # Increasing width of the frame
        self.expanded = False # Check if it is completely exanded
        self.isMoving = False # So we dont interupt the window resizement
        self.hasChanged = False        
        self.isLocked = tk.BooleanVar()

        # Define the icon to be shown and resize it
        self.plusImage = ImageTk.PhotoImage(Image.open("./data/images/plus.png").resize((40, 40)))

        self.root.update() # For the width to get updated

        tk.Frame.__init__(self, parent, bg=GREEN,width=50,height=root.winfo_height())
        self.pack(side="right", fill=tk.Y)

        
        self.plusImageObject = tk.Label(self, image=self.plusImage, bg=GREEN)


        self.plusImageObject.pack(fill="none", expand=True)

        # Bind to the frame, if entered or left
        self.bind('<Enter>',lambda e: self.expand() if self.isMoving is False else SetHasChanged())
        self.bind('<Leave>',lambda e: self.contract() if self.isMoving is False else SetHasChanged())

        self.frames={str:tk.Frame}
        self.frames["ConnectionFrame"] = self.CreateUserMenu(self, root)
        self.frames["AccountMenu"] = self.AccountMenu(self, root)

        self.activeFrame = "ConnectionFrame"
        self.frames["ConnectionFrame"].pack(fill="none", expand=True, anchor="center")

        def SetHasChanged():
            """
            Fix for menu not retracting if user is too fast
            """
            self.hasChanged = not self.hasChanged

        # So that it does not depend on the widgets inside the frame
        self.fill() # we run the method once to initialize everything
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
    
    def ChangeFrame(self, frameName:str):

        # remove current page
        self.frames[self.activeFrame].pack_forget()

        # sets up new frame
        self.activeFrame = frameName
        frame = self.frames[frameName]
        if self.expanded : frame.pack(expand=True, side="left")
        frame.tkraise()

    def fill(self)->None:
        if self.expanded: # If the frame is extended

            self.frames[self.activeFrame].pack(fill="none", expand=True, anchor="center")
            # Show everything, hide image
            self.plusImageObject.pack_forget()
            
        else:
            # hide everything
            self.frames[self.activeFrame].pack_forget()

            # Bring the image back
            self.plusImageObject.pack(fill="none", expand=True)
    
    class CreateUserMenu(tk.Frame):

        def __init__(self, parent:tk.Frame, root:App):
            parent.update_idletasks()
            tk.Frame.__init__(self, parent, bg=GREEN, width=50, height=parent.winfo_height())

            self.parent = parent
            self.root = root

            self.nameLabel = ttk.Label(self, text="Entrez votre prenom", background=GREEN)
            self.name = tk.StringVar()
            self.nameEntry = ttk.Entry(self, textvariable=self.name)

            self.name2Label = ttk.Label(self, text="Entrez votre nom : ", background=GREEN)
            self.name2 = tk.StringVar()
            self.name2Entry = ttk.Entry(self, textvariable=self.name2)

            self.idLabel = ttk.Label(self, text="Créez un identifiant : ", background=GREEN)
            self.id = tk.StringVar()
            self.idEntry = ttk.Entry(self, textvariable=self.id)

            # Creates the entries along with labels
            self.passwordLabel1 = ttk.Label(self, text="Créez un mot de passe", background=GREEN)
            self.password1, self.password2 = tk.StringVar(), tk.StringVar()
            self.passwordEntry1 = ttk.Entry(self, textvariable=self.password1, show="•")

            self.passwordLabel2 = ttk.Label(self, text="Confirmez le mot de passe", background=GREEN)
            self.passwordEntry2 = ttk.Entry(self, textvariable=self.password2, show="•")

            self.lockMenuButton = ttk.Checkbutton(self, variable=self.parent.isLocked, text="Bloquer le menu")

            self.confirmButton = ttk.Button(self, text="Créer", command=lambda : self.CreateUser(self.id.get(), self.password1.get(), self.password2.get(), self.name.get(), self.name2.get()))
            
            # place everything
            self.nameLabel.pack(side="top", pady=(35, 0))
            self.nameEntry.pack(side="top", pady=(0, 10))

            self.name2Label.pack(side="top", pady=(5, 0))
            self.name2Entry.pack(side="top", pady=(0, 10))

            self.idLabel.pack(side="top", pady=(10, 0))
            self.idEntry.pack(side="top", pady=(0, 25))

            self.passwordLabel1.pack(pady=(30, 0))
            self.passwordEntry1.pack(pady=(0, 10))

            self.passwordLabel2.pack()
            self.passwordEntry2.pack()

            self.lockMenuButton.pack(pady=(2, 2))
            self.confirmButton.pack(side="bottom")

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
                BDDapi.Nouveauclient(bdd, id, name2, name, psw1)
                bdd.commit()
                self.UserCreated()
            bdd.close()

    class AccountMenu(tk.Frame):

        def __init__(self, parent:tk.Frame, root:App):
            
            tk.Frame.__init__(self, parent, bg=GREEN, width=50, height=parent.winfo_height())

            self.parent:SideMenu = parent
            self.root:App = root

            self.NameLabel = ttk.Label(self, text="Default", background=GREEN)

            self.LogoutButton = ttk.Button(self, text="Se déconnecter", command=self.Logout)

            self.NameLabel.pack(side="left", pady=50)
            self.LogoutButton.pack(side="left")

        def RefreshText(self, newID):
            self.NameLabel.configure(text=newID)
            self.update_idletasks()

        def Logout(self):
            self.root.DisconnectClient()
            self.parent.ChangeFrame("ConnectionFrame")

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

        self.sideMenu = SideMenu(parent, self.root)        

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
            self.root.createUserSession(id)
            self.root.CreateStadiumFrames()
            self.root.show_frame("StadiumList")
            self.root.frames["StadiumList"].ShowButtons()
            self.sideMenu.ChangeFrame("AccountMenu")
            self.sideMenu.frames["AccountMenu"].RefreshText(self.root.client.GetClientId())
            return
        else:
            print("Hehe non")
            return


class CreateStadiumFrame(tk.Frame):

    def __init__(self, parent:tk.Frame, root:App):

        root.update_idletasks()
        # initialises Frame
        tk.Frame.__init__(self, parent, width=root.winfo_width()-root.winfo_width()//5, height=root.winfo_height(),
                           highlightbackground="black", highlightthickness=1, background=GREY)

        self.root = root

        # default values, will not be used, it's just for initialisation
        self.dimensionX = 100
        self.dimensionY = 50

        self.nameChoiceFrame = tk.Frame(self, background=GREY)

        pageNameLabel = ttk.Label(self, text="Creation Stade", background=GREY)
        pageNameLabel.pack(side="top")

        self.stadiumNameLabel = ttk.Label(self.nameChoiceFrame, text="Nom du nouveau stade: ", background=GREY)
        self.stadiumNameLabel.pack(side="top", pady=20)

        self.stadiumName = tk.StringVar()
        self.newStadiumNameEntry = ttk.Entry(self.nameChoiceFrame, textvariable=self.stadiumName)
        self.newStadiumNameEntry.pack(side="bottom")
        self.newStadiumNameEntry.focus()

        self.CapteursChoiceFrame = tk.Frame(self, background=GREY)

        self.stadiumImage = Graphs.DrawStadiumExample(1, 1)
        self.StadiumImageLabel = tk.Label(self.CapteursChoiceFrame, image=self.stadiumImage)

        self.XFrame = tk.Frame(self.CapteursChoiceFrame, highlightbackground="black", highlightthickness=1)
        self.YFrame = tk.Frame(self.CapteursChoiceFrame, highlightbackground="black", highlightthickness=1)

        self.xDim = tk.IntVar(value=1)
        self.xDim.trace_add("write", lambda e,a,z: self.RefreshStadium())
        self.yDim = tk.IntVar(value=1)
        self.yDim.trace_add("write", lambda e,a,z: self.RefreshStadium())
        self.dimensionBoxX = ttk.Combobox(self.XFrame, textvariable=self.xDim)
        self.dimensionBoxY = ttk.Combobox(self.YFrame, textvariable=self.yDim)    

        self.dimXLabel = ttk.Label(self.XFrame, text="Capteurs sur la longeur :")
        self.dimYLabel = ttk.Label(self.YFrame, text="Capteurs sur la largeur :")

        self.dimensionBoxX["values"] = [i for i in range(1, 21)]
        self.dimensionBoxY["values"] = [i for i in range(1, 11)]
        
        self.dimXLabel.pack(side="top")
        self.dimYLabel.pack(side="top")

        self.dimensionBoxX.pack(side="bottom")
        self.dimensionBoxY.pack(side="bottom")

        self.XFrame.pack(side="left")
        self.YFrame.pack(side="right", padx=50)

        self.StadiumImageLabel.pack(side="bottom", pady=(50, 0))

        self.nameChoiceFrame.pack(side="left", padx=(100, 0))
        self.CapteursChoiceFrame.pack(side="right", anchor="ne", pady=(100, 0))

        self.confirmButton = ttk.Button(self, text="Confirmer", command=self.CreateNewStadium)
        self.confirmButton.pack(side="bottom", anchor="s")

        self.ErrorLabel = ttk.Label(self, text = "Veuillez verifier vos entrées")

        self.pack_propagate(False)
    
    def RefreshStadium(self):
        self.stadiumImage = Graphs.DrawStadiumExample(self.xDim.get(), self.yDim.get())
        self.StadiumImageLabel.configure(image=self.stadiumImage)
        self.update_idletasks()
    
    def CreateNewStadium(self)->None:
        """
        Calls funtion to check in inputs are correct and calls App method to add the stadium
        """
        bdd = sqlite3.connect(self.root.BDDPATH)

        if BDDapi.CheckIfStadiumExists(bdd, self.stadiumName.get(), self.root.client.GetClientId()): # Check for duplicate name
            self.ErrorLabel.configure(text="Ce nom de stade existe deja !")
            self.update_idletasks()
            self.ErrorLabel.pack(side="left", anchor="sw")
            
        elif self.CheckValues(): #if everything is good

            # Add Stadium to BDD
            BDDapi.NewStadium(bdd, self.stadiumName.get(), (int(self.xDim.get()), int(self.yDim.get())), int(self.xDim.get())*int(self.yDim.get()), self.root.client.GetClientId())
            # Create Temps since 2000 for new Stadium
            BDDapi.InitializeNewStadium(bdd, self.stadiumName.get())

            bdd.commit()
            # Creates Stadium Frame
            self.root.AddStadiumFrame(self.stadiumName.get(), (int(self.xDim.get()), int(self.yDim.get())))
            # Shows new stadium Frame
            self.root.show_frame(self.stadiumName.get())
            
        else:
            self.ErrorLabel.configure(text="Veuillez verifier vos entrées")
            self.update_idletasks()
            self.ErrorLabel.pack(side="left", anchor="sw")

        bdd.close()
    
    def CheckValues(self)->bool:
        isGood = True

        # name must not be empty or just spaces
        if self.stadiumName.get().replace(" ", "") == "":
            isGood = False
            self.newStadiumNameEntry.delete(0, "end") # Removes text from entry
        try:
            # dimensions must not be empty or NaN
            self.dimensionX = int(self.xDim.get())
            self.dimensionY = int(self.xDim.get())
        except:
            isGood = False
            self.dimensionBoxX.delete(0, 'end')
            self.dimensionBoxY.delete(0, 'end')
            
        return isGood


class StadiumFrameTemplate(tk.Frame):

    def __init__(self, parent:tk.Frame, root:App, nomStade:str, dimentions):
        root.update_idletasks()
        # initialises Frame
        tk.Frame.__init__(self, parent, width=root.winfo_width()-root.winfo_width()//5, height=root.winfo_height(), highlightbackground="black", highlightthickness=1)
        self.root = root
        self.name = nomStade

        #create the stadium we'll get data from
        self.stade = Stade(nomStade, dimentions)
        self.calendar = tkcalendar.Calendar(self, locale="fr",day= (datetime.today() - timedelta(days=1)).day, maxdate=datetime.today() - timedelta(days=1))
        self.calendar.bind("<<CalendarSelected>>", lambda e: self.UpdateGraph())

        tk.Label(self, text=self.name).pack()

        self.graph = Figure(figsize=(5,3), dpi=100)
        self.graphCanvas = FigureCanvasTkAgg(self.graph, master=self)
        self.graphCanvas.draw()
        self.graphCanvas.get_tk_widget().pack(side="top", anchor="ne")

        self.calendar.pack(side="right", anchor="se")

        
        #self.refreshGraphButton = tk.Button(self, text="Refresh", command=self.updateGraph, font=("Helvetica", 25))
        #self.refreshGraphButton.pack(side="right", padx=30, pady=30)

        self.pack_propagate(False)

    def UpdateGraph(self):
        """
        returns image to show
        """
        # cette ligne est trop belle pour etre enlevée
        #imageData = np.array(gaussian_filter([[[0,(element+20)*7,0] for element in ligne] for ligne in data], sigma=0.75)).astype(np.uint8)
        
        self.graph.clf()
        self.axes = self.graph.add_subplot(111)
        hours = np.arange(24)
        bdd = sqlite3.connect(self.root.BDDPATH)
        dayMedium = BDDapi.GetMediumTemp(bdd, self.name, self.calendar.selection_get())
        temps = np.array([Graphs.CreateTemp(hour, dayMedium) for hour in hours])
        #print(hours, temps)
        self.axes.plot(hours, temps)
        
        # set fixed axes limits
        self.axes.set_xlim(0, 23)
        self.axes.set_ylim(-5, 30)

        self.graphCanvas.draw()

        #print("Tried to update graph")


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

        self.shownButtons:list[ttk.Button] = []

    def ShowButtons(self)->None:

        # On supprime les boutons affichés pour les remplacer
        for i in range(len(self.shownButtons)):
            item = self.shownButtons.pop(0)
            item.destroy()

        self.stadiumsToShow = self.root.client.GetClientStadiums()

        for stadium in self.stadiumsToShow:

            button = ttk.Button(self.displayWidget, text=stadium, command= lambda stadium=stadium: self.root.show_frame(stadium))
            button.pack()
            self.shownButtons.append(button)

        
if __name__ == "__main__":

    #App = StadiumFrameTemplate("Velodrome", 100, 50)
    #App.mainloop()

    palala = App()
    palala.mainloop()

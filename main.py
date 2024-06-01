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
from calendar import monthrange, isleap
from math import sqrt
from matplotlib.colors import TABLEAU_COLORS

from stades import Stade

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

        if type(frame) == StadiumFrameTemplate:
            frame.UpdateGraph()

        if type(frame) == StadiumListFrame:
            frame.ShowButtons()

    def AddStadiumFrame(self, name, dimensions=("10", "5")):
        if name in ["HomeFrame", "CreateStadium", "StadiumList"]:
            return
        self.frames[name] = StadiumFrameTemplate(self.container, self, name, (int(dimensions[0]), int(dimensions[1])))

    def createUserSession(self, id):
        if self.client is not None:
            print("Error, existing session running")
            return
        else:
            self.client = Client(self, id)    
    
    def CreateStadiumFrames(self):

        stadiumList = self.client.GetClientStadiums()
        for stadium in stadiumList:
            self.AddStadiumFrame(stadium[0], stadium[1].split("x"))

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
        self.stadiumList:list[tuple[str, tuple[int, int]]] = []
        self.RefreshClientStadiums()
        
    def GetClientId(self)->str:
        return self.id
    
    def GetClientStadiums(self)->list[tuple[str, str]]:
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
        self.root.update() # For the width to get updated
        self.min_w = self.root.winfo_width()//15 # Minimum width of the frame
        self.max_w = self.root.winfo_width()//5 # Maximum width of the frame
        self.cur_width = self.min_w # Increasing width of the frame
        self.expanded = False # Check if it is completely exanded
        self.isMoving = False # So we dont interupt the window resizement
        self.hasChanged = False        
        self.isLocked = tk.BooleanVar()

        # Define the icon to be shown and resize it
        self.plusImage = ImageTk.PhotoImage(Image.open("./data/images/plus.png").resize((40, 40)))


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

            self.userInfoFrame = tk.Frame(self, highlightbackground="black", highlightthickness=1)

            self.userName = ttk.Label(self.userInfoFrame, text="Default")

            self.changePasswordLabel1 = ttk.Label(self.userInfoFrame, text="Changer votre mot de passe :")
            self.password1 = tk.StringVar()
            self.changePasswordEntry1 = ttk.Entry(self.userInfoFrame, textvariable=self.password1, show="•")

            self.changePasswordLabel2 = ttk.Label(self.userInfoFrame, text="Confirmer le mot de passe")
            self.password2 = tk.StringVar()            
            self.changePasswordEntry2 = ttk.Entry(self.userInfoFrame, textvariable=self.password2, show="•")

            self.confirmPasswordChange = ttk.Button(self.userInfoFrame, text="Confirmer", command=self.ConfirmPasswordChange)

            self.homeButton = ttk.Button(self, text="Menu", command= lambda : self.root.show_frame("StadiumList"))
            self.LogoutButton = ttk.Button(self, text="Se déconnecter", command=self.Logout)

            self.passwordMismachLabel = ttk.Label(self, text="Mots de passe differents", background="red")
            self.passwordChangeSucces = ttk.Label(self, text="Mot de passe changé avec succès !", background="green")

            self.userName.pack(side="top")
            self.changePasswordLabel1.pack(side="top")
            self.changePasswordEntry1.pack(side="top", pady=(0, 3))
            self.changePasswordLabel2.pack(side="top")
            self.changePasswordEntry2.pack(side="top", pady=(0, 4))
            self.confirmPasswordChange.pack(side="top")

            self.homeButton.pack(pady=(0, 20))
            self.userInfoFrame.pack(pady=100)
            
            self.LogoutButton.pack(expand= True, fill = "none")

        def RefreshText(self, newID):
            self.userName.configure(text=newID)
            self.update_idletasks()

        def Logout(self):


            self.root.DisconnectClient()
            self.parent.ChangeFrame("ConnectionFrame")

        def MismatchPasswordError(self):
            self.passwordMismachLabel.pack(side="bottom", pady=(0, 4))
            self.after(2000, self.passwordMismachLabel.pack_forget)

        def PasswordChangeSuccces(self):            
            self.passwordChangeSucces.pack(side="bottom", pady=(0, 4))
            self.after(2000, self.passwordChangeSucces.pack_forget)

        def ConfirmPasswordChange(self):
            if self.password1.get() != self.password2.get():
                self.MismatchPasswordError()
            else:
                bdd = sqlite3.connect(self.root.BDDPATH)
                BDDapi.ChangeUserPassword(bdd, self.root.client.GetClientId(), self.password1.get())
                bdd.commit()
                bdd.close()

                self.PasswordChangeSuccces()


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

        self.logMessage = ttk.Label(self)

    def LoginUser(self, id, psw)->None:
        bdd = sqlite3.connect(self.root.BDDPATH)
        access = BDDapi.connection(bdd, id, psw)
        bdd.close()

        if access:
            self.showLogMessage("Connecté avec succès, veuillez patienter ...", "green")
            self.root.createUserSession(id)
            self.root.CreateStadiumFrames()
            self.root.show_frame("StadiumList")
            self.root.frames["StadiumList"].ShowButtons()
            self.sideMenu.ChangeFrame("AccountMenu")
            self.sideMenu.frames["AccountMenu"].RefreshText(self.root.client.GetClientId())
        else:
            self.showLogMessage("Erreur, veuillez verifiez vos identifiants et mot de passe.", "red")

    def showLogMessage(self, text, color):
        self.logMessage.configure(text=text, background=color)
        self.update_idletasks()
        self.logMessage.pack(side="top", pady=(3, 0))
        self.after(2000, self.logMessage.pack_forget)


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
        self.stadiumNameLabel.pack(side="top", pady=12)

        self.stadiumName = tk.StringVar()
        self.newStadiumNameEntry = ttk.Entry(self.nameChoiceFrame, textvariable=self.stadiumName)
        self.newStadiumNameEntry.pack()
        self.newStadiumNameEntry.focus()

        self.CapteursChoiceFrame = tk.Frame(self, background=GREY)
        self.ImageExampleFrame = tk.Frame(self.CapteursChoiceFrame, background= GREY)

        self.stadiumImage = Graphs.DrawStadiumExample(1, 1)
        self.StadiumImageLabel = tk.Label(self.ImageExampleFrame, image=self.stadiumImage)

        self.XFrame = tk.Frame(self.CapteursChoiceFrame, highlightbackground="black", highlightthickness=1)
        self.YFrame = tk.Frame(self.CapteursChoiceFrame, highlightbackground="black", highlightthickness=1)

        self.xDim = tk.IntVar(value=1)
        self.xDim.trace_add("write", lambda e,a,z: self.RefreshStadium())
        self.yDim = tk.IntVar(value=1)
        self.yDim.trace_add("write", lambda e,a,z: self.RefreshStadium())
        self.dimensionBoxX = ttk.Combobox(self.XFrame, textvariable=self.xDim, state="readonly")
        self.dimensionBoxY = ttk.Combobox(self.YFrame, textvariable=self.yDim, state="readonly")    

        self.dimXLabel = ttk.Label(self.XFrame, text="Capteurs sur la longeur :")
        self.dimYLabel = ttk.Label(self.YFrame, text="Capteurs sur la largeur :")

        self.dimensionBoxX["values"] = [i for i in range(1, 11)]
        self.dimensionBoxY["values"] = [i for i in range(1, 6)]
        
        self.dimXLabel.pack(side="top")
        self.dimYLabel.pack(side="top")

        self.dimensionBoxX.pack(side="bottom")
        self.dimensionBoxY.pack(side="bottom")

        self.XFrame.pack(side="top")
        self.YFrame.pack(side="top")

        self.StadiumImageLabel.pack(side="bottom", pady=(50, 0))

        self.nameChoiceFrame.pack(side="left", padx=(100, 0))
        self.CapteursChoiceFrame.pack(side="right", anchor="ne", pady=(100, 0), padx=(0, 20))
        self.ImageExampleFrame.pack(side="bottom", anchor = "s")

        self.confirmButton = ttk.Button(self.nameChoiceFrame, text="Confirmer", command=self.CreateNewStadium)
        self.confirmButton.pack(side="bottom", pady=(10, 0))

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

        self.stadiumNameFrame = tk.Frame(self, highlightbackground="black", highlightthickness=1)
        self.graphFrame = tk.Frame(self, highlightbackground="black", highlightthickness=1)
        self.configureStadiumFrame = tk.Frame(self, highlightbackground="black", highlightthickness=1)

        def GetBoolStateString(state):
            if state:
                return "On"
            return "Off"
        
        self.isHeating = tk.BooleanVar(value=False)
        self.heatingLabel = ttk.Label(self.configureStadiumFrame, text="Chauffage : " + GetBoolStateString(self.isHeating.get()))
        self.heatingButton = ttk.Button(self.configureStadiumFrame, text="Allumer / Eteindre", command= lambda : (self.isHeating.set( not self.isHeating.get()),
                                                                                                        self.heatingLabel.configure(text="Chauffage : " + GetBoolStateString(self.isHeating.get()))))
                                                                                                        #, self.update_idletasks()))
        
        self.arrosage = tk.BooleanVar(value=False)
        self.arrosageLabel = ttk.Label(self.configureStadiumFrame, text="Arrosage : " + GetBoolStateString(self.arrosage.get()))
        self.arrosageButton = ttk.Button(self.configureStadiumFrame, text="Allumer / Eteindre", command= lambda : (self.arrosage.set( not self.arrosage.get()),
                                                                                                        self.arrosageLabel.configure(text="Arrosage : " + GetBoolStateString(self.arrosage.get()))))
                                                                                                        #, self.update_idletasks()))        
        
        self.showSeuil = tk.BooleanVar(value=False)
        self.showSeuilLabel = ttk.Label(self.configureStadiumFrame, text="Seuils : " + GetBoolStateString(self.showSeuil.get()))
        self.showSeuilButton = ttk.Button(self.configureStadiumFrame, text="Montrer / Cacher", command= lambda : (self.showSeuil.set(not self.showSeuil.get()),
                                                                                                            self.showSeuilLabel.configure(text="Seuils : " + GetBoolStateString(self.showSeuil.get()))))

        self.dimText = f"   Capteurs: \nLongueur: {dimentions[0]}\nLargeur: {dimentions[1]}"
        self.repartitionCapteursLabel = ttk.Label(self.configureStadiumFrame, text = self.dimText)
        
        self.isHeating.trace_add("write", lambda e,a,z: self.UpdateGraph())
        self.arrosage.trace_add("write",lambda e,a,z: self.UpdateGraph())
        self.showSeuil.trace_add("write", lambda e,a,z: self.UpdateGraph())

        self.repartitionCapteursLabel.pack(side="top", pady=(3, 0))

        self.stadiumNameLabel = ttk.Label(self.stadiumNameFrame, text=self.name, font="Bold 30")

        self.showTodayBool = tk.BooleanVar(value=False)
        self.showToday = ttk.Checkbutton(self.graphFrame, text="Aujourd'hui", variable=self.showTodayBool, command= lambda : self.UpdateGraph(True))
        #self.showTodayBool.trace_add("write", lambda e, a, z: self.ToggleTodayGraph(self.showTodayBool.get()))
        
        self.graph = Figure(figsize=(6.8,4.2), dpi=100)
        self.calendar = tkcalendar.Calendar(self, locale="fr",day= (datetime.today() - timedelta(days=1)).day, maxdate=datetime.today() - timedelta(days=1),
                                            background=GREY, selectbackground = GREEN, font="Arial 12", foreground="black")
        self.calendar.selection_set(datetime.today() - timedelta(1))
        self.graphCanvas = FigureCanvasTkAgg(self.graph, master=self.graphFrame)
        self.graphCanvas.draw()

        self.modeChoice = tk.StringVar()
        self.modeSelection = ttk.Combobox(self.graphFrame, values=["Jour", "Mois", "Année"], textvariable=self.modeChoice, state="readonly")
        self.modeSelection.current(0)
        self.modeChoice.trace_add("write", lambda e,a,z: self.UpdateGraph())
        #create the stadium we'll get data from
        self.stade = Stade(nomStade, dimentions)
        self.calendar.bind("<<CalendarSelected>>", lambda e: self.UpdateGraph())

        #region InfoCapteurs

        self.capteurInfoFrame = ScrolledFrame(self, width = 500, height = 200, scrollbars = "vertical", use_ttk = True)        
        self.capteurInfoFrame.bind_arrow_keys(self.root)
        self.capteurInfoFrame.bind_scroll_wheel(self.root)

        self.displayCapteur = self.capteurInfoFrame.display_widget(tk.Frame)
        self.capteurs:list[tk.Button] = []
        nbCapteurs = self.stade.GetSize()
        for i in range(nbCapteurs[0]):
            for j in range(nbCapteurs[1]):
                self.capteurs.append(ttk.Label(self.displayCapteur, text= f"Capteur {str(i+j)} : {0}°C"))

        #endregion

        self.heatingLabel.pack(side="top")
        self.heatingButton.pack(side="top")
        self.arrosageLabel.pack(side="top", pady=(10, 0))
        self.arrosageButton.pack(side="top", pady=(0, 10))

        self.stadiumNameLabel.pack()
        self.repartitionCapteursLabel.pack()

        self.graphCanvas.get_tk_widget().pack(anchor="e")
        self.modeSelection.pack(side="left", padx=(5), pady=2)
        self.showToday.pack(side="right", padx=(5), pady=2)

        self.capteurInfoFrame.grid(column=1, row=5, columnspan=4, rowspan=3, padx=20, pady=30)
        self.graphFrame.grid(column=1, row=0, columnspan=5, rowspan=3, padx=(0,10), pady=(10, 0))
        self.calendar.grid(column=5, row=4, padx=(0,10), pady=(10, 10), sticky = "E")
        self.stadiumNameFrame.grid(column=2, row=4, pady=30)
        self.configureStadiumFrame.grid(column=0, row=1, padx=(10,10), pady=(10, 0))

        self.pack_propagate(False)
        self.grid_propagate(False)


        self.ToggleTodayGraph(self.showTodayBool.get())

    def ToggleTodayGraph(self, state):

        if state: # If we only want to show today's temps
            self.calendar.grid_remove()
            self.stadiumNameFrame.grid_remove()
            self.modeSelection.pack_forget()
            self.capteurInfoFrame.grid()
            self.showSeuilLabel.pack(side="top")
            self.showSeuilButton.pack(side="top")
        else:
            self.capteurInfoFrame.grid_remove()
            self.stadiumNameFrame.grid()
            self.calendar.grid()
            self.modeSelection.pack(side="left", padx=(5), pady=2)            
            self.showSeuilLabel.pack_forget()
            self.showSeuilButton.pack_forget()

    def UpdateGraph(self, isToggling=False):
        """
        Refreshes graph
        """
        # cette ligne est trop belle pour etre enlevée
        #imageData = np.array(gaussian_filter([[[0,(element+20)*7,0] for element in ligne] for ligne in data], sigma=0.75)).astype(np.uint8)
        
        try:
            self.graph.clf()
        except:
            return
        if isToggling:
            self.ToggleTodayGraph(self.showTodayBool.get())

        self.axes = self.graph.add_subplot(111)
        isPredicting = (False, 24)
        if(self.showTodayBool.get()):            

            nbValeurs = np.arange(datetime.now().hour + 1)
            bdd = sqlite3.connect(self.root.BDDPATH)
            dayMedium = BDDapi.GetMediumTemp(bdd, self.name, datetime.now().date())
            temps = np.array([Graphs.CreateDayTemp(hour, dayMedium) for hour in nbValeurs])


            isPredicting = (True, nbValeurs.size-1)
            for hour in range(nbValeurs.size, 24):
                nbValeurs = np.append(nbValeurs, hour)
                temps = np.append(temps, Graphs.CreateDayTemp(hour, dayMedium+ 7*self.isHeating.get() - 5*self.arrosage.get()))
            bdd.close()

        else:
            match self.modeSelection.get():
                case "Jour":
                    nbValeurs = np.arange(24)
                    bdd = sqlite3.connect(self.root.BDDPATH)
                    dayMedium = BDDapi.GetMediumTemp(bdd, self.name, self.calendar.selection_get())
                    temps = np.array([Graphs.CreateDayTemp(hour, dayMedium) for hour in nbValeurs])
                    precip = np.array([Graphs.CreateDayPrecip(hour, self.calendar.selection_get().day,self.calendar.selection_get().month,dayMedium) for hour in nbValeurs])
                    precax=self.axes.twinx()
                    precax.set_ylim(0, 100)
                    precax.set_ylabel("Precipitation (mm)", color="green")
                    precax.plot(nbValeurs, precip,"C2",label="Precipitation")
                    bdd.close()

                case "Mois":
                    bdd = sqlite3.connect(self.root.BDDPATH)
                    nbValeurs = np.arange(monthrange(*self.calendar.get_displayed_month()[::-1])[1])            
                    temps = np.array(BDDapi.GetTempsInMonth(bdd, self.name, *self.calendar.get_displayed_month()))
                    bdd.close()

                case "Année":
                    bdd = sqlite3.connect(self.root.BDDPATH)
                    nbValeurs = np.arange(365 + isleap(self.calendar.selection_get().year))
                    temps = np.array(BDDapi.GetTempsInYear(bdd, self.name, self.calendar.get_displayed_month()[1]))
                    bdd.close()
                case _:
                    print("Ho no")

        if isPredicting[0]:
            self.axes.plot(nbValeurs[:isPredicting[1]], temps[:isPredicting[1]], label="Mesures", linewidth=2)
            self.axes.plot(nbValeurs[isPredicting[1]-1:], temps[isPredicting[1]-1:], "g--", label="Prédictions", linewidth=2)

            if self.showSeuil.get():
                self.axes.plot(nbValeurs, [25]*len(nbValeurs), "r-.", linewidth=.5)
                self.axes.plot(nbValeurs, [5]*len(nbValeurs), "r-.", linewidth=.5)

            # On crée d'autres temperatures pour faire croire que tous les capteurs marchent
            # Plus il y a de capteurs plus les tempratures sont proches
            for i, element in enumerate(self.capteurs):
                element.configure(text=f"Capteur {i+1} : {Graphs.CreateDayTemp(datetime.now().hour, dayMedium)- sqrt((i//5)**2 + (i%5)**2)* 0.07:.2f}°C")
                element.grid(row=i//5, column=i%5)
                element.update_idletasks()
            
            leg = self.axes.legend(loc="lower right")
            for line in leg.get_lines():
                line.set_linewidth(2)
        else:
            self.axes.plot(nbValeurs, temps)

        # set fixed axes limits
        self.axes.set_xlim(0, max(len(nbValeurs)-1, 23))
        self.axes.set_ylim(-5, 35)
        self.axes.set_xlabel("Jour")
        self.axes.set_ylabel("Temps (C°)", color=TABLEAU_COLORS["tab:blue"])
        self.graphCanvas.draw()

        #self.update_idletasks()

    def createNewTempFromDefault(self, oldtemps):
        rep = []
        if oldtemps[0]%2 == 1:
            sign = 1
        else:
            sign = -1

        toAdd = int(str((oldtemps[0]**2)*sign)[:3])/200
        for temp in oldtemps:
            rep.append(temp + toAdd)
        return np.array(rep)


class StadiumListFrame(tk.Frame):

    def __init__(self, parent:tk.Frame, root:App):
        
        tk.Frame.__init__(self, parent)
        self.root = root
        self.parent = parent

        self.listFrame = ttk.Frame(self)

        self.yourStadiumsLabel = ttk.Label(self.listFrame, text="Vos stades :", font="TkTextFont 20")
        self.yourStadiumsLabel.pack(side="top", pady=(0, 5))

        self.list = ScrolledFrame(self.listFrame, width = 400, height = 200, scrollbars = "vertical", use_ttk = True)
        self.list.bind_arrow_keys(self.root)
        self.list.bind_scroll_wheel(self.root)
        self.list.pack(side="bottom")
        self.displayWidget = self.list.display_widget(tk.Frame)

        self.listFrame.pack(side="left")

        self.createStadiumBUtton = ttk.Button(self, text="Creer un nouveau stade", command=lambda : root.show_frame("CreateStadium"))
        self.createStadiumBUtton.pack(side="right")

        self.shownButtons:list[ttk.Button] = []


    def ShowButtons(self)->None:

        # On supprime les boutons affichés pour les remplacer
        for i in range(len(self.shownButtons)):
            item = self.shownButtons.pop(0)
            item.destroy()
        self.root.client.RefreshClientStadiums()
        self.stadiumsToShow = self.root.client.GetClientStadiums()

        for stadium in self.stadiumsToShow:
            button = ttk.Button(self.displayWidget, text=stadium[0], command= lambda stadium=stadium[0]: self.root.show_frame(stadium))
            button.pack()
            self.shownButtons.append(button)

        
if __name__ == "__main__":

    #App = StadiumFrameTemplate("Velodrome", 100, 50)
    #App.mainloop()

    palala = App()
    palala.mainloop()

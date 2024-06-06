import tkinter as tk
from tkinter import ttk

import Graphs
import sqlite3
import BDDapi

from colors import GREY

class CreateStadiumFrame(tk.Frame):
    """
    Stadium creation Frame
    """
    def __init__(self, parent:tk.Frame, root):

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

        self.stadiumNameLabel = ttk.Label(self.nameChoiceFrame, text="Nom du nouveau stade", background=GREY)
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
        self.yDim = tk.IntVar(value=1)
        self.xDim.trace_add("write", lambda e,a,z: self.RefreshStadium())
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

        self.XFrame.grid(column=1, row=0)
        self.YFrame.grid(column=2, row=0)

        self.StadiumImageLabel.pack(side="bottom", pady=(50, 0))

        self.nameChoiceFrame.pack(side="left", padx=(100, 0))
        self.CapteursChoiceFrame.pack(side="right", anchor="ne", pady=(100, 0), padx=(0, 20))
        self.ImageExampleFrame.grid(column=0, row=3, rowspan=3, columnspan=4, pady=(50, 0))

        self.confirmButton = ttk.Button(self.nameChoiceFrame, text="Confirmer", command=self.CreateNewStadium)
        self.confirmButton.pack(side="bottom", pady=(10, 0))

        self.ErrorLabel = ttk.Label(self, text = "Veuillez verifier vos entrées")

        self.pack_propagate(False)
    
    def RefreshStadium(self):
        """
        met a jour l'affichage des capteurs
        """
        self.stadiumImage = Graphs.DrawStadiumExample(self.xDim.get(), self.yDim.get())
        self.StadiumImageLabel.configure(image=self.stadiumImage)
        self.update_idletasks()
    
    def CreateNewStadium(self)->None:
        """
        Calls funtion to check in inputs are correct and calls App method to add the stadium
        """
        bdd = sqlite3.connect(self.root.BDDPATH)

        if BDDapi.CheckIfStadiumExists(bdd, self.stadiumName.get(), self.root.client.GetClientId()): # Check for duplicate name
            self.ErrorLabel.configure(text="Ce nom de stade existe déjà !")
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

            self.stadiumName.set("")

            self.xDim.set(1)
            self.yDim.set(1)
            
        else:
            self.ErrorLabel.configure(text="Veuillez vérifier vos entrées")
            self.update_idletasks()
            self.ErrorLabel.pack(side="left", anchor="sw")

        bdd.close()
    
    def CheckValues(self)->bool:
        """
        verifie si les données entrées sont valides, retourne True or False
        """
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


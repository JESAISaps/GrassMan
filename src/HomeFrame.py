import tkinter as tk
from tkinter import ttk

from SideMenu import SideMenu
import sqlite3
import BDDapi

class HomeFrame(tk.Frame):
    """
    Connection frame
    """
    def __init__(self, parent:tk.Frame, root):

        tk.Frame.__init__(self, parent)
        # reference to controller main window, might be usefulls
        self.root = root
        self.parent = parent
        self.userId = tk.StringVar()
        self.idInput = ttk.Entry(self, textvariable=self.userId)
        self.idInputLabel = ttk.Label(self, text="Identifiant")

        self.password = tk.StringVar()
        self.passwordInput = ttk.Entry(self, textvariable=self.password, show="•")
        self.passwordInputLabel = ttk.Label(self, text="Mot de passe")

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
            self.userId.set("")
            self.password.set("")
        else:
            self.showLogMessage("Erreur, veuillez vérifiez vos identifiants et mot de passe.", "red")

    def showLogMessage(self, text, color):
        self.logMessage.configure(text=text, background=color)
        self.update_idletasks()
        self.logMessage.pack(side="top", pady=(3, 0))
        self.after(2000, self.logMessage.pack_forget)


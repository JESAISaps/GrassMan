import tkinter as tk
from tkinter import ttk

import sqlite3
import BDDapi


from PIL import Image, ImageTk

from colors import GREEN

class SideMenu(tk.Frame):
    """
    Menu on the right
    """
    def __init__(self, parent, root):
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
        self.plusImage = ImageTk.PhotoImage(Image.open("./src/data/images/plus.png").resize((40, 40)))


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
        """
        agrandit le menu
        """
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
        """
        retrecie le menu
        """
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
        """
        change la page du menu
        """

        # remove current page
        self.frames[self.activeFrame].pack_forget()

        # sets up new frame
        self.activeFrame = frameName
        frame = self.frames[frameName]
        if self.expanded : frame.pack(expand=True, side="left")
        frame.tkraise()

    def fill(self)->None:
        """
        vide ou rempli le menu selon s'il est agrandit ou retrecit
        """
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
        """
        Page de creation du compte
        """
        def __init__(self, parent:tk.Frame, root):
            parent.update_idletasks()
            tk.Frame.__init__(self, parent, bg=GREEN, width=50, height=parent.winfo_height())

            self.parent = parent
            self.root = root

            self.nameLabel = ttk.Label(self, text="Entrez votre prénom", background=GREEN)
            self.name = tk.StringVar()
            self.nameEntry = ttk.Entry(self, textvariable=self.name)

            self.name2Label = ttk.Label(self, text="Entrez votre nom", background=GREEN)
            self.name2 = tk.StringVar()
            self.name2Entry = ttk.Entry(self, textvariable=self.name2)

            self.idLabel = ttk.Label(self, text="Créez un identifiant", background=GREEN)
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

            self.name.set("")
            self.name2.set("")
            self.id.set("")
            self.password1.set("")
            self.password2.set("")

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
        """
        Page d'infos du compte, avec le changement dan mdp, le retour au menu, et la deconnexion
        """
        def __init__(self, parent:tk.Frame, root):
            
            tk.Frame.__init__(self, parent, bg=GREEN, width=50, height=parent.winfo_height())

            self.parent:SideMenu = parent
            self.root = root

            self.userInfoFrame = tk.Frame(self, highlightbackground="black", highlightthickness=1)

            self.userName = ttk.Label(self.userInfoFrame, text="Default")

            self.changePasswordLabel1 = ttk.Label(self.userInfoFrame, text="Changer votre mot de passe")
            self.password1 = tk.StringVar()
            self.changePasswordEntry1 = ttk.Entry(self.userInfoFrame, textvariable=self.password1, show="•")

            self.changePasswordLabel2 = ttk.Label(self.userInfoFrame, text="Confirmer le mot de passe")
            self.password2 = tk.StringVar()            
            self.changePasswordEntry2 = ttk.Entry(self.userInfoFrame, textvariable=self.password2, show="•")

            self.confirmPasswordChange = ttk.Button(self.userInfoFrame, text="Confirmer", command=self.ConfirmPasswordChange)

            self.homeButton = ttk.Button(self, text="Menu", command= lambda : self.root.show_frame("StadiumList"))
            self.LogoutButton = ttk.Button(self, text="Se déconnecter", command=self.Logout)

            self.passwordMismachLabel = ttk.Label(self, text="Mot de passe différent", background="red")
            self.passwordChangeSucces = ttk.Label(self, text="Mot de passe changé avec succès !", background="green")            
            self.lockMenuButton = ttk.Checkbutton(self, variable=self.parent.isLocked, text="Bloquer le menu")

            self.userName.pack(side="top")
            self.changePasswordLabel1.pack(side="top")
            self.changePasswordEntry1.pack(side="top", pady=(0, 3))
            self.changePasswordLabel2.pack(side="top")
            self.changePasswordEntry2.pack(side="top", pady=(0, 4))
            self.confirmPasswordChange.pack(side="top")

            self.homeButton.pack(pady=(0, 20))
            self.userInfoFrame.pack(pady=100)
            self.lockMenuButton.pack()
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

            self.password2.set("")
            self.password1.set("")

        def ConfirmPasswordChange(self):
            if self.password1.get() != self.password2.get():
                self.MismatchPasswordError()
            else:
                bdd = sqlite3.connect(self.root.BDDPATH)
                BDDapi.ChangeUserPassword(bdd, self.root.client.GetClientId(), self.password1.get())
                bdd.commit()
                bdd.close()

                self.PasswordChangeSuccces()


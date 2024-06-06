import tkinter as tk
from tkinter import ttk
from tkscrolledframe import ScrolledFrame

class StadiumListFrame(tk.Frame):
    """
    Intermediate window for stadium choice
    """
    def __init__(self, parent:tk.Frame, root):
        
        tk.Frame.__init__(self, parent)
        self.root = root
        self.parent = parent

        self.listFrame = ttk.Frame(self)

        self.yourStadiumsLabel = ttk.Label(self.listFrame, text="Vos stades", font="TkTextFont 20")
        self.yourStadiumsLabel.pack(side="top", pady=(0, 5))

        self.list = ScrolledFrame(self.listFrame, width = 400, height = 200, scrollbars = "vertical", use_ttk = True)
        self.list.bind_arrow_keys(self.root)
        self.list.bind_scroll_wheel(self.root)
        self.list.pack(side="bottom")
        self.displayWidget = self.list.display_widget(tk.Frame)

        self.listFrame.pack(side="left")

        self.createStadiumBUtton = ttk.Button(self, text=" Créer un nouveau stade ", command=lambda : root.show_frame("CreateStadium"))
        self.createStadiumBUtton.pack(side="right")

        self.shownButtons:list[ttk.Button] = []


    def ShowButtons(self)->None:
        """
        affiche les boutons, appelé apres pour que le client existe
        """
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


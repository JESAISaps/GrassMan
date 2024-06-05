from HomeFrame import HomeFrame
from CreateStadiumFrame import CreateStadiumFrame
from StadiumFrameTemplate import StadiumFrameTemplate
from StadiumListFrame import StadiumListFrame
from Client import Client

import tkinter as tk
from tkinter import Tk

class App(Tk):
    """
    Main window
    """
    def __init__(self):

        self.BDDPATH = "./src/data/bddstade.db"
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

        
if __name__ == "__main__":

    palala = App()
    palala.mainloop()

import sqlite3
import BDDapi

class Client:
    """
    Contains informations about current connected client
    """
    def __init__(self, root, id=None):
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


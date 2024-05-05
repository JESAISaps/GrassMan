import sqlite3
import stades

class BDD():

    def __init__(self) -> None:
        self.bdd = sqlite3.connect("./data/bddstade.db").cursor()
        self.stade = stades.Stade("Velodrome")
        self.Tmap=self.stade.getTemp()
        self.Meteo=self.stade.GetMeteo()
        self.Lightmap=self.stade.GetSoleil()

#    def remplirtemp(self,listeTemp):

    def remplircapteur(self):
        longueur = self.stade.longueur
        largeur = self.stade.largeur
        nombrecapteur=longueur*largeur 
        id=0 
        for ligne in range(longueur):
            for colonne in range(largeur):
                self.bdd.execute("INSERT INTO Capteurs values ("+longueur+","+largeur+",1,"+id+")")
                id=id+1


# condition vraie seulement si ce script est celui qui a ete run, Faux si il est run dans un import
if __name__ == "__main__":
    BDD1=BDD()
    BDD1.test()

    BDD1.remplircapteur

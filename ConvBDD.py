import sqlite3
import stades

class BDD():

    def __init__(self,saison) -> None:
        #self.bdd = sqlite3.connect("./data/bddstade.db")
        self.stade = stades.Stade("Velodrome",saison,*[50,100])
        self.Tmap=self.stade.getTemp()
        self.Meteo=self.stade.GetMeteo()
        self.Lightmap=self.stade.GetSoleil()
        #self.bdd.close()

#    def remplirtemp(self,listeTemp):

    def remplircapteur(self):
        self.bdd = sqlite3.connect("C:/Users/mar38/Documents/GitHub/GrassMan/data/bddstade.db")
        longueur = self.stade.longueur
        largeur = self.stade.largeur
        nombrecapteur=longueur*largeur 
        id=0 
        for ligne in range(longueur):
            for colonne in range(largeur):
                self.bdd.execute("INSERT INTO Capteurs values ("+str(ligne)+","+str(colonne)+",1,"+str(id)+")")
                id=id+1
        self.bdd.commit()
        self.bdd.close()

# condition vraie seulement si ce script est celui qui a ete run, Faux si il est run dans un import
if __name__ == "__main__":
    BDD1=BDD("hiver")
    BDD1.remplircapteur()

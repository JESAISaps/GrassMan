from random import choice

class Stade:

    def __init__(self, nom:str, dimensions) -> None:
        self.nom = nom
        self.longueur = dimensions[0]
        self.largeur = dimensions[1]

        self.meteo = self.createMeteo()

        self.capteurs = [[(i, j) for j in range(dimensions[0]) for i in range(dimensions[1])]]    

    def createBlankStadium(self, x, y):
        """
        Cree une matrice nulle de dimension yx
        """
        return [[0] * x for _ in range(y)]
    
    def gestionarrosage(self):
        """
        Retourne Vrai si on arrose le stade et Faux sinon
        """
        for i in range (len(self.temperature1)):
                    for k in range(len(self.temperature1[i])):
                        if (self.temperature1[i][k]) >=25 :
                            return True 
        return False

    def createMeteo(self):
        """""
        Renvoie une météo aléatoire
        """
        meteoAleatoire = choice(["ensoleille","nuageux","pluie","neige","brouillard"])
        return(meteoAleatoire)

    def modifMeteo(self):
        """
        Modifie la météo, modifie la variable et adapte l'ouverture du toit si besoin
        """
        self.meteo = self.createMeteo()

    def modifSoleil(self):
        """
        Modifie la variable ensoleillement 
        """
        self.ensoleillement = self.soleil()
        
        #print("done modifying list")

    def GetSoleil(self):
        """
        retourne la variable ensoleillement 
        """
        return self.ensoleillement

    def GetMeteo(self):
        """
        retourne la variable meteo 
        """
        return self.meteo

    def GetSize(self):
        """
        retourne la variable taille du stade sous la forme d'un tuple
        """
        return self.longueur, self.largeur
          
    def GetIdStade(self,bddstade):
        #bddstade=sqlite3.connect("./data/bddstade.db")
        #bdd=bddstade.cursor()
        #idstade=bdd.execute("Select IdStade from Stade where Nom='"+self.nom+"'").fetchall()
        #return idstade[0][0]
        return self.nom

        

# condition vraie seulement si ce script est celui qui a ete run, Faux si il est run dans un import
if __name__ == "__main__":
    s = Stade("Velodrome",(50,100))
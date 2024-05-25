import random
from math import floor
import sqlite3
class Stade:

    def __init__(self, nom:str, dimensions,) -> None:
        self.nom = nom
        self.longueur = dimensions[0]
        self.largeur = dimensions[1]
        self.temperature1 = self.CreateTemp([1,0,2018])
        self.ensoleillement = self.soleil()
        self.meteo = self.createMeteo()
        self.isRoofClosed = self.changeRoofState()
        self.chauffage = self.gestionchauffage()
        self.arrosage = self.gestionarrosage()

    def createBlankStadium(self, x, y):
        """
        Cree une matrice nulle de dimension yx
        """
        return [[0] * x for _ in range(y)]


    def changeRoofState(self):
        """
        Retourne Vrai si on ferme le stade et Faux sinon
        """
        if self.meteo == "pluie" or self.meteo == "neige":
            return True
        else :
            return False
        
    def gestionchauffage(self):
        """
        Retourne Vrai si on chauffe le stade et Faux sinon
        """
        for i in range (len(self.temperature1)):
                    for k in range(len(self.temperature1[i])):
                        if (self.temperature1[i][k]) <=10 :
                            return True 
        return False
    
    def gestionarrosage(self):
        """
        Retourne Vrai si on arrose le stade et Faux sinon
        """
        for i in range (len(self.temperature1)):
                    for k in range(len(self.temperature1[i])):
                        if (self.temperature1[i][k]) >=25 :
                            return True 
        return False
    
    def moyenneTemp(self,listetemperature):
        somme = 0
        nombre_valeurs = 0
        for k in range(len(listetemperature)):
            for valeur in range(len(listetemperature[k])):
                somme=(somme+listetemperature[k][valeur])
                nombre_valeurs = nombre_valeurs + 1
        moyenne = somme/nombre_valeurs
        return(moyenne)
    

    def soleil(self):
        """
        Fonction qui va pas tarder a degager
        """
        listeSoleil = self.createBlankStadium(self.longueur, self.largeur)
        for ligne in listeSoleil:
            for k in range(len(ligne)):
                    soleilHiver = random.randint(0,1)
                    ligne[k] = soleilHiver
        return(listeSoleil)

    def createMeteo(self):
        """""
        Renvoie une météo aléatoire
        """
        meteoAleatoire = random.choice(["ensoleille","nuageux","pluie","neige","brouillard"])
        return(meteoAleatoire)

    def modifMeteo(self):
        """
        Modifie la météo, modifie la variable et adapte l'ouverture du toit si besoin
        """
        self.meteo = self.createMeteo()
        self.isRoofClosed = self.changeRoofState()

    def modifSoleil(self):
        """
        Modifie la variable ensoleillement 
        """
        self.ensoleillement = self.soleil()

    def modifTemp(self):
        """
        Modifie la variable temperature 
        """
        #self.temperature1 = self.temperature() # temperature modifiée aléatoirement
        #print("starting modifying list")
        if self.gestionchauffage() == True :
             for k in range(len(self.temperature1)):
                  for i in range(len(self.temperature1[k])):
                        self.temperature1[k][i] = self.temperature1[k][i]+2
        if self.gestionarrosage() == True :
             for k in range(len(self.temperature1)):
                  for i in range(len(self.temperature1[k])):
                        self.temperature1[k][i] = self.temperature1[k][i]-2
        
        #print("done modifying list")


    def getTemp(self):
        """
        retourne la variable temperature 
        """
        return self.temperature1

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
    
    def GetMooveRoof(self):
        if self.meteo == "pluie" or self.meteo == "neige":
            return("closed")
        else :
            return("open")
          
    def GetIdStade(self,bddstade):
        bddstade=sqlite3.connect("./data/bddstade.db")
        bdd=bddstade.cursor()
        idstade=bdd.execute("Select IdStade from Stade where Nom='"+self.nom+"'").fetchall()
        return idstade[0][0]
      
    def CreateTemp(self,Date):
        Moyenne=[3.7,4.4,8.1,11.7,15.6,20.2,22.6,22.1,18,13.6,8,4.5]
        Mois=Date[1]
        Jour=Date[0]
        listeTemp = self.createBlankStadium(self.longueur, self.largeur)
        TempDepart=Moyenne[Mois]+random.uniform(-0.4,0.4)
        if Mois!=11:
            TempDepart=TempDepart+(Moyenne[Mois+1]+random.uniform(-0.2,0.2)-TempDepart)*Jour/31
        else:
            TempDepart=TempDepart+(Moyenne[0]+random.uniform(-0.2,0.2)-TempDepart)*Jour/31
        tempMax = abs(TempDepart +0.2)
        for o in range(len(listeTemp)):                
            for k in range(len(listeTemp[o])):
                # on va faire une temperature qui depend de celles créées précédement, à proximité de l'element actuel
                # cas limites aux bord de la matrice
                if o==0 and k==0:
                    temperature=TempDepart
                elif o==0:
                    temperature = listeTemp[o][k-1]+random.uniform(-0.5,0.5)
                elif k==0:
                    temperature = sum([listeTemp[o-1][k], listeTemp[o-1][k+1]])/2+random.uniform(-0.5,0.5)
                elif k==len(listeTemp[o])-1:
                    temperature = sum([listeTemp[o-1][k-1], listeTemp[o-1][k],listeTemp[o][k-1]])/3+random.uniform(-0.5,0.5)
                else : 
                    temperature = sum([listeTemp[o-1][k-1], listeTemp[o-1][k],listeTemp[o][k-1],listeTemp[o-1][k+1]])/4+random.uniform(-0.5,0.5)
                        
                if abs(temperature) > abs(tempMax):
                        # On ajuste temperature a tempMax si ça depasse et on lui redonne son signe
                    temperature = tempMax * temperature/abs(temperature)
                listeTemp[o][k]=temperature
        return(listeTemp)
        
# condition vraie seulement si ce script est celui qui a ete run, Faux si il est run dans un import
if __name__ == "__main__":
    s = Stade("Velodrome",(50,100))
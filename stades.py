from random import randint, choice

class Stade:

    def __init__(self, nom:str, longueur:int=100, largeur:int=50) -> None:
        self.nom = nom
        self.longeur = longueur
        self.largeur = largeur
        self.temperature1 = self.ajustemp()
        self.ensoleillement = self.soleil()
        self.meteo = self.createMeteo()
    def createBlankStadium(self, x, y):
        return [[0] * x for _ in range(y)]

    def temperature(self):
        listeTemp = self.createBlankStadium(self.longeur, self.largeur)
        for ligne in listeTemp:
            for k in range(len(ligne)):
                    temperatureHiver = randint(-10,10)
                    ligne[k] = temperatureHiver
        return(listeTemp)

    def ajustemp(self):
        listeTemp = self.createBlankStadium(self.longeur, self.largeur)
        Temp0 = randint(-10,10)
        listeTemp[0][0]=Temp0
        for o in range(len(listeTemp)):                
            for k in range(len(listeTemp[o])):
                if o==0 and k==0:
                    temperature=Temp0
                elif o==0:
                    temperature =listeTemp[o][k-1]+randint(-1,1)
                elif k==0:
                    temperature =listeTemp[o-1][k]+randint(-1,1)
                else : 
                    temperature =listeTemp[o-1][k-1]+randint(-1,1)
                listeTemp[o][k] = temperature
        print(listeTemp)
        return(listeTemp)

    def soleil(self):
        listeSoleil = self.createBlankStadium(self.longeur, self.largeur)
        for ligne in listeSoleil:
            for k in range(len(ligne)):
                    soleilHiver = randint(0,1)
                    ligne[k] = soleilHiver
        return(listeSoleil)

    def createMeteo(self):
        meteoAleatoire = choice(["ensoleille","nuageux","pluie","neige","brouillard"])
        return(meteoAleatoire)

    def modifMeteo(self):
         self.meteo = self.createMeteo()

    def modifSoleil(self):
         self.ensoleillement = self.soleil()

    def modifTemp(self):
         self.temperature1 = self.temperature()

    def getTemp(self):
         return self.temperature1

    def GetSoleil(self):
         return self.soleil

    def GetMeteo(self):
         return self.meteo

    def GetSize(self):
         return self.longeur, self.largeur
    



# condition vraie seulement si ce script est celui qui a ete run, Faux si il est run dans un import
if __name__ == "__main__":
    
    s = Stade("Velodrome")
    s.ajustemp()

from random import randint, choice

class Stade:

    def __init__(self, nom) -> None:
        self.nom = nom
        self.temperature1 = self.temperature()
        self.ensoleillement = self.soleil()
        self.meteo = self.createMeteo

    def createBlankStadium(self, x, y):
        return [[0] * y for _ in range(x)]
    
    def temperature(self):
        listeTemp = self.createBlankStadium(100, 50)
        for ligne in listeTemp:
            for k in range(len(ligne)):
                    temperatureHiver = randint(-10,10)
                    ligne[k] = temperatureHiver
        return(listeTemp)
    
    def soleil(self):
        listeSoleil = self.createBlankStadium(100, 50)
        for ligne in listeSoleil:
            for k in range(len(ligne)):
                    soleilHiver = randint(0,1)
                    ligne[k] = soleilHiver
        return(listeSoleil)
    
    def createMeteo(self):
        meteoAleatoire = choice("ensoleille","nuageux","pluie","neige","brouillard")
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



if __name__ == "__main__":
    
    s = Stade("Velodrome")



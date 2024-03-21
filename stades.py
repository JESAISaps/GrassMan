from random import randint, choice

class Stade:

    def __init__(self, nom) -> None:
        self.nom = nom
        self.tempMap = self.temperature()
        self.lightMap = self.soleil()
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
                    soleilHiver = randint(-10,10)
                    ligne[k] = soleilHiver
        return(listeSoleil)
    
    def createMeteo(self):
        meteoAleatoire = choice("ensoleille","nuageux","pluie","neige","brouillard")
        return(meteoAleatoire)
       

if __name__ == "__main__":
    
    s = Stade("Velodrome")



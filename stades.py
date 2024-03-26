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
        
        # tempMax limite la variation de temperature a 2 * la 
        # temperature de depart sur l'ensemble du terrain
        tempMax = abs(Temp0*2)
        for o in range(len(listeTemp)):                
            for k in range(len(listeTemp[o])):
                if o==0 and k==0:
                    temperature=Temp0
                elif o==0:
                    temperature = listeTemp[o][k-1]+randint(-1,1)
                elif k==0:
                    temperature = sum([listeTemp[o-1][k], listeTemp[o-1][k+1]])/2+randint(-1,1)
                elif k==len(listeTemp[o])-1:
                    temperature = sum([listeTemp[o-1][k-1], listeTemp[o-1][k],listeTemp[o][k-1]])/3+randint(-1,1)
                else : 
                    temperature = sum([listeTemp[o-1][k-1], listeTemp[o-1][k],listeTemp[o][k-1],listeTemp[o-1][k+1]])/4+randint(-1,1)
                if abs(temperature) > abs(tempMax):
                     # On ajuste temperature a tempMax et on lui redonne son signe
                     temperature = tempMax * temperature/abs(temperature)
                listeTemp[o][k] = temperature
        #print(listeTemp)
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
         return self.ensoleillement

    def GetMeteo(self):
         return self.meteo

    def GetSize(self):
         return self.longeur, self.largeur
    



# condition vraie seulement si ce script est celui qui a ete run, Faux si il est run dans un import
if __name__ == "__main__":
    
    s = Stade("Velodrome")
    s.ajustemp()
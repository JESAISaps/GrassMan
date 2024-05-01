import sqlite3
import stades

class BDD():

    def __init__(self) -> None:
        self.bdd = sqlite3.connect("./data/bddstade.db").cursor()
        self.stade = stades.Stade("Velodrome")
        self.Tmap=self.stade.getTemp()
        self.Meteo=self.stade.GetMeteo()
        self.Lightmap=self.stade.GetSoleil()

    def createbdd(self):
        self.bdd.execute('CREATE TABLE Temperature (CoX INTEGER,CoY INTEGER,Temperature INTEGER NOT NULL,PRIMARY KEY (CoX,CoY))')
        self.bdd.execute('CREATE TABLE Eclairage (CoX INTEGER,CoY INTEGER,Lumiere INTEGER NOT NULL,PRIMARY KEY (CoX,CoY))')
        self.bdd.execute('CREATE TABLE Meteo (Meteo TEXT PRIMARY KEY);')
        self.bdd.commit()
        
    def remplirbdd(self):
        for k in range(len(self.Tmap)):
            for i in range(len(self.Tmap[k])):
                self.bdd.execute('INSERT INTO Temperature values ('+str(k)+','+str(i)+','+str(self.Tmap[k][i])+')')
                self.bdd.commit()
        for k in range(len(self.Lightmap)):
            for i in range(len(self.Lightmap[k])):
                self.bdd.execute('INSERT INTO Eclairage values ('+str(k)+','+str(i)+','+str(self.Lightmap[k][i])+')')
                self.bdd.commit()
    
    def test(self):
        for k in range(len(self.Tmap)):
            for i in range(len(self.Tmap[k])):
                print('INSERT INTO Temperature values ('+str(k)+','+str(i)+','+str(self.Tmap[k][i])+')')
        for k in range(len(self.Lightmap)):
            for i in range(len(self.Lightmap[k])):
                self.bdd.execute('INSERT INTO Eclairage values ('+str(k)+','+str(i)+','+str(self.Lightmap[k][i])+')')




# condition vraie seulement si ce script est celui qui a ete run, Faux si il est run dans un import
if __name__ == "__main__":
    BDD1=BDD()
    BDD1.test()


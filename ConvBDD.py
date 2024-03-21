import sqlite3
import stades

class BDD():

    def __init__(self) -> None:
        self.bdd = sqlite3.connect("./data/bdd.db").cursor()
        self.stade = stades.Stade("Velodrome")
        self.Tmap=self.stade.tempMap
        self.Meteo=self.stade.meteo
        self.Lightmap=self.stade.lightMap

    def createbdd(self):
        self.bdd.execute('CREATE TABLE Temperature (CoX INTEGER,CoY INTEGER,Temperature INTEGER NOT NULL,PRIMARY KEY (CoX,CoY))')

    def remplirbdd(self):
        for k in range(len(self.Tmap)):
            for i in range(len(self.Tmap[k])):
                self.bdd.execute('INSERT INTO Temperature values ('+str(k)+','+str(i)+','+str(self.Tmap[k][i])+')')

    def test(self):
        for k in range(len(self.Tmap)):
            for i in range(len(self.Tmap[k])):
                print('INSERT INTO Temperature values ('+str(k)+','+str(i)+','+str(self.Tmap[k][i])+')')

BDD1=BDD()
BDD1.test()

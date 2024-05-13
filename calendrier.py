import sqlite3
import stades

bdd=sqlite3.connect("C:/Users/mar38/Documents/GitHub/GrassMan/data/bddstade.db")
def associerdatetemperature():
    listejour=bdd.execute('Select Jour from Temperature').fetchall()
    if listejour==[]:
        return 1
    else:
        return listejour[len(listejour)][0]+1
    
def recupidcapteur(x,y):
    idcapteur=bdd.execute('Select IdCapteurs from Capteurs where PositionX='+str(x)+' and PositionY='+str(y)).fetchall()
    return idcapteur[0][0]
    
def importtemperature(listetemp):
    for ligne in range (len(listetemp)):
        for colonne in range(len(listetemp[ligne])):
                idcapteur=recupidcapteur(ligne,colonne)
                bdd.execute('INSERT INTO Temperature values ('+str(associerdatetemperature())+','+str(listetemp[ligne][colonne])+','+str(idcapteur)+')')
    bdd.commit()
    bdd.close()


importtemperature(stades.CreateFirstTempMap(50,100))
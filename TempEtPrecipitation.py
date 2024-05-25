import stades
import sqlite3
import random
from math import floor

def AssocierDateTemperature(bddstade,Stade):
        bdd=bddstade.cursor()
        listejour=bdd.execute("Select Jour from Temperature,Capteurs WHERE Temperature.IdCapteurs = Capteurs.IdCapteurs and Capteurs.IdStade= "+str(Stade.GetIdStade(bddstade))).fetchall()
        if listejour==[]:
            return 1
        else:
            return listejour[len(listejour)-1][0]+1
        
Moyenne=[3.7,4.4,8.1,11.7,15.6,20.2,22.6,22.1,18,13.6,8,4.5]
Precipitation=[27,26.6,30,31.8,31.8,23.7,20.7,20.7,32.2,37,46.6,27]

def RecupIdcapteur(x,y,idstade,bddstade):
    bdd=bddstade.cursor()
    idcapteur=bdd.execute('Select IdCapteurs from Capteurs where PositionX= '+str(x)+' and PositionY= '+str(y)+' and IdStade= '+str(idstade)).fetchall()
    return idcapteur[0][0]

def ImportTemperature(listetemp,bddstade,Stade):
        jour=AssocierDateTemperature(bddstade,Stade)
        bdd=bddstade.cursor()
        for ligne in range (len(listetemp)):
            for colonne in range(len(listetemp[ligne])):
                    idcapteur=RecupIdcapteur(ligne,colonne,Stade.GetIdStade(bddstade),bddstade)
                    bdd.execute('INSERT INTO Temperature values ('+str(jour)+','+str(listetemp[ligne][colonne])+','+str(idcapteur)+')')

def Temperature(Stade,bddstade,Moyenne):
    Jour=AssocierDateTemperature(bddstade,Stade)
    Jour=230
    while Jour>365:
        Jour=Jour-365
    Mois=int(Jour//31)
    Jour=Jour-31*Mois

    listeTemp = Stade.createBlankStadium(Stade.longueur, Stade.largeur)
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
   


    


if __name__ == "__main__":
    s = stades.Stade("Velodrome",(100,50),"hiver")
    bdd = sqlite3.connect("./data/bddstade.db")
    for k in range(5):
        Temperature(s,bdd,Moyenne)
        #ImportTemperature(Temperature(s,bdd,Moyenne),bdd,s)
    bdd.commit()
    bdd.close()
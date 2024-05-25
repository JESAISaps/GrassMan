import bcrypt
import stades
import sqlite3
from datetime import datetime, timedelta
from random import uniform

def connection(bdd, id,mdp):
    bddstade = bdd.cursor()

    if CheckIfIdExists(bdd, id):
        command = "SELECT motdepasse FROM client WHERE identifiant = ?;"
        vraimdp = bddstade.execute(command, (id,)).fetchall()[0][0]

        if bcrypt.checkpw(mdp.encode("utf-8"), vraimdp.encode("utf-8")):
            return True
        else:
            return False
    return None
        
    #bdd.close()

def CheckIfIdExists(bdd, id):
    #bdd = sqlite3.connect("./data/bddstade.db")
    bddstade = bdd.cursor()

    clientidentifiant=bddstade.execute('SELECT identifiant FROM client;').fetchall()
    #print(clientidentifiant)
    knownIdList = [ligne[0] for ligne in clientidentifiant]
    #print(knownIdList)
    #print(id)
    if id in knownIdList:
        return True
    return False

def nouveauclient(bdd, id,name,name1,motdepasse):
    #bdd = sqlite3.connect("./data/bddstade.db")
    psw = motdepasse.encode("utf-8")
    bddstade = bdd.cursor()
    command = "INSERT INTO client VALUES (?, ?, ?, ?);"
    bddstade.execute(command, (name1, name, id, str(bcrypt.hashpw(psw, bcrypt.gensalt()))[2:-1]))
    #bdd.close()

def NewStadium(bdd:sqlite3.Connection, name:str, size:tuple, nbCapteurs:int, clientID:str):
    bddStade = bdd.cursor()

    command = "INSERT INTO stade VALUES (?, ?, ?, ?);"
    bddStade.execute(command, (name, str(size)[1:-1], nbCapteurs, clientID))

def CheckIfStadiumExists(bdd:sqlite3.Connection, name:str, clientID:str):
    bddstade = bdd.cursor()

    # Returns True if Stadium name already taken
    return name in [ligne[0] for ligne in bddstade.execute('SELECT Nom FROM stade WHERE clientID = ?;', (clientID,)).fetchall()]

def GetClientStadiums(bdd:sqlite3.Connection, clientID:str)->list[str]:
    """
    Renvoie les stades qui appartiennent au client clientID
    """
    bddStade = bdd.cursor()
    rep = []
    command = "SELECT Nom FROM stade WHERE clientID = ?;"
    temp = bddStade.execute(command, (clientID,)).fetchall()
    for stadium in temp:
        rep.append(stadium)
    return rep

def associerdatetemperature(bddstade):
    bdd=bddstade.cursor()
    listejour=bdd.execute('Select Jour from Temperature;').fetchall()
    if listejour==[]:
        return 1
    else:
        return listejour[len(listejour)-1][0]+1
    
def recupidcapteur(x,y,idstade,bddstade):
    bdd=bddstade.cursor()
    idcapteur=bdd.execute('Select IdCapteurs from Capteurs where PositionX= '+str(x)+' and PositionY= '+str(y)+' and IdStade= '+str(idstade)).fetchall()
    print(idcapteur)
    return idcapteur[0][0]
      
def importtemperature(listetemp,bddstade,nomstade,idstade):
    jour=associerdatetemperature(bddstade)
    bdd=bddstade.cursor()
    for ligne in range (len(listetemp)):
        print(len(listetemp[ligne]))
        for colonne in range(len(listetemp[ligne])):
                idcapteur=recupidcapteur(ligne,colonne,idstade,bddstade)
                bdd.execute('INSERT INTO Temperature values ('+str(jour)+','+str(listetemp[ligne][colonne])+','+str(idcapteur)+');')

def InitializeNewStadium(bdd, name):
    """
    Creates the temps since 2000, is only called from outside on stadium creation
    """
    passedDays= CreateDaysHistory()
    temps = CreateOldTemps(passedDays)
    AddOldTempsToDB(bdd, temps, name)
    
def CreateDaysHistory():
    rep = []
    for year in range(2000, datetime.now().year + 1):
        start_date=datetime(year, 1, 1)
        end_date=datetime(year, 12, 31)
        d=start_date
        while d <= end_date:
            rep.append(d)
            d += timedelta(days=1)
    return rep

def AddOldTempsToDB(bdd:sqlite3.Connection, temps, name:str):
    bddstade = bdd.cursor()
    command = "INSERT INTO Temperature VALUES (?, ?, ?);"
    for day in temps:
        bddstade.execute(command, (name, *day))

def CreateOldTemps(passedDays):
    rep = []
    for day in passedDays:
        rep.append((day, CreateTemp((day.day, day.month))))
    return rep
    
def CreateTemp(Date):
    Moyenne=[3.7,4.4,8.1,11.7,15.6,20.2,22.6,22.1,18,13.6,8,4.5]
    Mois=Date[1]-1 # On fait -1 car les dates commencent a 1
    Jour=Date[0]-1
    TempDepart=Moyenne[Mois]+uniform(-0.4,0.4)
    if Mois!=11:
        TempDepart=TempDepart+(Moyenne[Mois+1]+uniform(-0.2,0.2)-TempDepart)*Jour/31
    return TempDepart

if __name__ == "__main__":
    #password = "HelloWorld".encode("utf-8")
    #hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    #command = f"{hashed}"
    #print(hashed, type(hashed))
    #print(command)
    s= stades.Stade("Velodrome",(100,50),"hiver")
    bdd = sqlite3.connect("./data/bddstade.db")
    importtemperature(s.CreateFirstTempMap("hiver"),bdd,"Velodrome",s.GetIdStade())
    bdd.commit()

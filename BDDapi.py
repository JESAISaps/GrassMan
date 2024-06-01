import bcrypt
import stades
import sqlite3
from datetime import datetime, timedelta
import Graphs
from random import uniform, randint

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

def CheckIfIdExists(bdd, id):
    bddstade = bdd.cursor()

    clientidentifiant=bddstade.execute('SELECT identifiant FROM client;').fetchall()
    knownIdList = [ligne[0] for ligne in clientidentifiant]
    if id in knownIdList:
        return True
    return False

def Nouveauclient(bdd, id,name,name1,motdepasse):
    psw = motdepasse.encode("utf-8")
    bddstade = bdd.cursor()
    command = "INSERT INTO client VALUES (?, ?, ?, ?);"
    bddstade.execute(command, (name1, name, id, str(bcrypt.hashpw(psw, bcrypt.gensalt()))[2:-1]))
    #bdd.close()

def NewStadium(bdd:sqlite3.Connection, name:str, size:tuple, nbCapteurs:int, clientID:str):
    bddStade = bdd.cursor()

    command = "INSERT INTO stade VALUES (?, ?, ?, ?);"
    bddStade.execute(command, (name, str(size[0]) + "x" + str(size[1]), nbCapteurs, clientID))

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
    command = "SELECT Nom, Taille FROM stade WHERE clientID = ?;"
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
    #print(idcapteur)
    return idcapteur[0][0]
      
def importtemperature(listetemp,bddstade,nomstade,idstade):
    jour=associerdatetemperature(bddstade)
    bdd=bddstade.cursor()
    for ligne in range (len(listetemp)):
        #print(len(listetemp[ligne]))
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
    dif = randint(-5, 5) #Facon avec laquelle tous les stades n'ont pas une temp moyenne trop proche
    for day in passedDays:
        rep.append((day, dif + Graphs.CreateTemp((day.day, day.month, day.year))))
    return rep


def GetMediumTemp(bdd:sqlite3.Connection, stadium:str, day:datetime) -> int:
    bdd.set_trace_callback(print)
    bddStade = bdd.cursor()

    command = "SELECT Temperature from Temperature WHERE Stade = ? AND Jour = ?;"
    rep = bddStade.execute(command, (stadium, str(day) + " 00:00:00")).fetchall()[0][0]
    print(rep)
    return rep

def GetTempsInMonth(bdd, stade, month, year):
    bddStade = bdd.cursor()
    rep = []
    command = "SELECT TEMPERATURE FROM TEMPERATURE WHERE JOUR LIKE ? AND Stade = ?"
    
    if month < 10:
        temp = bddStade.execute(command, (str(year)+ "-0" + str(month)+ "%", stade)).fetchall()
    else:
        temp = bddStade.execute(command, (str(year)+ "-" + str(month)+ "%", stade)).fetchall()
    for value in temp:
        rep.append(value[0])
    return rep


def GetTempsInYear(bdd, stade, year):
    bddStade = bdd.cursor()
    rep = []
    command = "SELECT TEMPERATURE FROM TEMPERATURE WHERE JOUR LIKE ? AND Stade = ?;"
    temp = bddStade.execute(command, (str(year) + "%", stade)).fetchall()
    for value in temp:
        rep.append(value[0])
    return rep

def ChangeUserPassword(bdd:sqlite3.Connection, userId, newPass):
    bddStade = bdd.cursor()
    command = "UPDATE client SET motdepasse = ? WHERE identifiant = ?;"
    bddStade.execute(command, (str(bcrypt.hashpw(newPass.encode("utf-8"), bcrypt.gensalt()))[2:-1], userId))


if __name__ == "__main__":
    
    s= stades.Stade("Velodrome",(100,50),"hiver")
    bdd = sqlite3.connect("./data/bddstade.db")
    importtemperature(s.CreateFirstTempMap("hiver"),bdd,"Velodrome",s.GetIdStade())
    bdd.commit()

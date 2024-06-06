import bcrypt
import sqlite3
from datetime import datetime, timedelta
import Graphs
from random import randint

def connection(bdd, id,mdp):
    """
    return True si la connection est possible, avec le mot de passe et idClient.
    """
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
    """
    return True si l'id existe dans la base
    """
    bddstade = bdd.cursor()

    clientidentifiant=bddstade.execute('SELECT identifiant FROM client;').fetchall()
    knownIdList = [ligne[0] for ligne in clientidentifiant]
    if id in knownIdList:
        return True
    return False

def Nouveauclient(bdd, id,name,name1,motdepasse):
    """
    insere un nouveau client dans la table client
    """
    bddstade = bdd.cursor()
    psw = motdepasse.encode("utf-8")
    command = "INSERT INTO client VALUES (?, ?, ?, ?);"
    bddstade.execute(command, (name1, name, id, str(bcrypt.hashpw(psw, bcrypt.gensalt()))[2:-1]))

def NewStadium(bdd:sqlite3.Connection, name:str, size:tuple, nbCapteurs:int, clientID:str):
    bddStade = bdd.cursor()

    command = "INSERT INTO stade VALUES (?, ?, ?, ?);"
    bddStade.execute(command, (name, str(size[0]) + "x" + str(size[1]), nbCapteurs, clientID))

def CheckIfStadiumExists(bdd:sqlite3.Connection, name:str, clientID:str):
    """
    return True si le stade name existe dans stade
    """
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

def InitializeNewStadium(bdd, name):
    """
    Crée des temperatures depuis l'annee 2000, et demande de les ajouter dans la bdd
    """
    passedDays= CreateDaysHistory()
    temps = CreateOldTemps(passedDays)
    AddOldTempsToDB(bdd, temps, name)

def CreateDaysHistory():
    """
    retourne une liste des dates depuis l'an 2000
    """
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
    """
    ajoute dans la table Temperatures les temperatures du stade name
    """
    bddstade = bdd.cursor()
    command = "INSERT INTO Temperature VALUES (?, ?, ?);"
    for day in temps:
        bddstade.execute(command, (name, *day))

def CreateOldTemps(passedDays):
    """
    crée une liste des temperatures depuis l'an 2000
    """
    rep = []
    dif = randint(-5, 5) #Facon avec laquelle tous les stades n'ont pas une temp moyenne trop proche
    for day in passedDays:
        rep.append((day, dif + Graphs.CreateTemp((day.day, day.month, day.year))))
    return rep

def GetMediumTemp(bdd:sqlite3.Connection, stadium:str, day:datetime) -> int:
    """
    retourne la temperature du jour day, du stade stadium
    """
    #bdd.set_trace_callback(print)
    bddStade = bdd.cursor()

    command = "SELECT Temperature from Temperature WHERE Stade = ? AND Jour = ?;"
    rep = bddStade.execute(command, (stadium, str(day) + " 00:00:00")).fetchall()[0][0]
    return rep

def GetTempsInMonth(bdd, stade, month, year):
    """
    renvoie une liste des temperatures du mois month et annee year, du stade stade
    """
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
    """
    renvoie une liste des temperatures de l'annee annee du stade stade
    """
    bddStade = bdd.cursor()
    rep = []
    command = "SELECT TEMPERATURE FROM TEMPERATURE WHERE JOUR LIKE ? AND Stade = ?;"
    temp = bddStade.execute(command, (str(year) + "%", stade)).fetchall()
    for value in temp:
        rep.append(value[0])
    return rep

def ChangeUserPassword(bdd:sqlite3.Connection, userId, newPass):
    """
    change le mot de passe de l'utilisateur userId avec le mdp newPass
    """
    bddStade = bdd.cursor()
    command = "UPDATE client SET motdepasse = ? WHERE identifiant = ?;"
    bddStade.execute(command, (str(bcrypt.hashpw(newPass.encode("utf-8"), bcrypt.gensalt()))[2:-1], userId))

import bcrypt
import stades
import sqlite3
def connection(bdd, id,mdp):
    #bdd = sqlite3.connect("./data/bddstade.db")
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

    clientidentifiant=bddstade.execute('SELECT identifiant FROM client').fetchall()
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

def GetClientStadiums(bdd, client)->list[str]:
    #TODO: Choper le nom des stades qui apartiennent au client et la renvoyer
    return ["Velodrome", "Chez ton pere"] #en attendant

def associerdatetemperature(bddstade):
    bdd=bddstade.cursor()
    listejour=bdd.execute('Select Jour from Temperature').fetchall()
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
                bdd.execute('INSERT INTO Temperature values ('+str(jour)+','+str(listetemp[ligne][colonne])+','+str(idcapteur)+')')

if __name__ == "__main__":
    password = "HelloWorld".encode("utf-8")
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    command = f"{hashed}"
    print(hashed, type(hashed))
    print(command)
    s= stades.Stade("Velodrome",(100,50),"hiver")
    bdd = sqlite3.connect("./data/bddstade.db")
    importtemperature(s.CreateFirstTempMap("hiver"),bdd,"Velodrome",s.GetIdStade())
    bdd.commit()

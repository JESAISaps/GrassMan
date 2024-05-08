import sqlite3
import bcrypt


def connection(bdd, id,mdp):
    #bdd = sqlite3.connect("./data/bddstade.db")
    bddstade = bdd.cursor()

    if CheckIfIdExists(bdd, id):
        command = "SELECT motdepasse FROM client WHERE identifiant = '{identifiant}';"
        #print(command)
        vraimdp=bddstade.execute(command.format(identifiant=id)).fetchall()[0][0]
        #print(mdp.encode("utf-8"))
        #print(vraimdp.encode("utf-8"))
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
    print(clientidentifiant)
    knownIdList = [ligne[0] for ligne in clientidentifiant]
    print(knownIdList)
    if id in knownIdList:
        return True
    return False

def nouveauclient(bdd, id,name,name1,motdepasse):
    #bdd = sqlite3.connect("./data/bddstade.db")
    psw = motdepasse.encode("utf-8")
    bddstade = bdd.cursor()
    command = "INSERT INTO client VALUES ('{nom}', '{prenom}','{identifiant}','{password}');"
    #print(command.format(nom=name1, prenom=name, identifiant=id, password=str(bcrypt.hashpw(psw, bcrypt.gensalt()))[2:-1]))
    bddstade.execute(command.format(nom=name1, prenom=name, identifiant=id, password=str(bcrypt.hashpw(psw, bcrypt.gensalt()))[2:-1]))
    #bdd.close()

if __name__ == "__main__":
    password = "HelloWorld".encode("utf-8")
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    command = f"{hashed}"
    print(hashed, type(hashed))
    print(command)
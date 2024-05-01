import sqlite3
import bcrypt


def connection(identifiant,mdp):
    bdd = sqlite3.connect("./data/bddstade.db")
    bddstade = bdd.cursor()

    clientidentifiant=bddstade.execute('SELECT identifiant FROM client').fetchall()
    knownIdList = [ligne[0] for ligne in clientidentifiant]
    if identifiant in knownIdList:
        vraimdp=bddstade.execute('SELECT motdepasse from client where identifiant = '+identifiant).fetchall()[0][0]
        if bcrypt.checkpw(mdp, vraimdp):
            return True
        else:
            return False
    bdd.close()

def nouveauclient(identifiant,nom,prenom,motdepasse,idstade):
    bdd = sqlite3.connect("./data/bddstade.db")
    bddstade = bdd.cursor()
    bddstade.execute('INSERT INTO client values ("'+nom+'", "'+prenom+'","'+identifiant+'","'+str(idstade)+'","'+bcrypt.hashpw(motdepasse, bcrypt.gensalt())+'")')

    bdd.commit()
    bdd.close()

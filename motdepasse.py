import sqlite3
bdd = sqlite3.connect("./data/bddstade.db")

idclient=input("identifiant")
clientidentifiant=bdd.execute('SELECT identifiant from client')

if idclient in clientidentifiant:
    print("kk")
else:
    bdd.execute('INSERT INTO nomclient ('+idclient+')')
                  
nom=input("nom")
prenom=input("prénom")

bdd.commit
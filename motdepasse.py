import sqlite3
bddstade = sqlite3.connect("./data/bddstade.db")

identifiant=input("identifiant")
clientidentifiant=bddstade.execute('SELECT identifiant from client')

#if idclient in clientidentifiant:
#    print("kk")
#else:
#    bddstade.execute('INSERT INTO nomclient ('+idclient+')')
                  
nom=input("nom:")
prenom=input("prénom:")
stade=input("stade:")
motdepasse=input("mot de passe:")

bddstade.execute('INSERT INTO client ('+nom+', '+prenom+','+identifiant+','+stade+','+motdepasse+')')


bddstade.commit()
from PIL import Image, ImageTk
import numpy as np
from scipy.ndimage import gaussian_filter
from random import randint, uniform, choice
from matplotlib import image as matim
import math

def aleatoire(a):
    """
    Retourne un nobre pseudo-aleatoire entre 0 et 9, a l'aide de la seed a
    """
    return int(str(abs((np.exp(a**1.2))%997)*5.3)[0])

def CreateDayTemp(heure, dayMedium)->int:
    """
    Renvoie une temperature selon une heure et une moyenne d'un jour.
    """
    rep = dayMedium-2 + np.sin(heure*np.pi/12 +aleatoire(dayMedium)/12+4.5)*6
    
    return rep

def CreateDayPrecip(heure, jour, Mois, dayMediumTemp)->int:
    """
    Crée les precipitations d'une journée a l'aide de pseudo-aleatoire, se basant sur tous les arguments.
    """
    Moyenne=[20,25,60,70,40,15,12,10,20,80,75,34]
    dayMedium=Moyenne[Mois-1]
    if int((dayMedium-jour+aleatoire(dayMedium)))%3==0:
        return 0
    rep =0.1*aleatoire(heure+dayMediumTemp+jour*0.1)*(+dayMedium-2 + heure/6 + np.sin(np.pi/12 +dayMediumTemp/6 +1+(heure*jour*np.pi+heure/(jour+1)))*6)
    
    return rep

def RechauffementClimatique(Moyenne,Date):
    """
    modifie une temperature Moyenne selon sa date Date pour simuler du
    rechaufement climatique
    """
    if Date[2]>2000:
        for k in range(len(Moyenne)):
            Moyenne[k]=Moyenne[k]+math.log(Moyenne[k]/10*(Date[2]-2000),10)
    return Moyenne
                    
def CreateTemp(Date):
    """
    Renvoie une temperature (int) pseudo aleatoire qui depend de la date en argument, sous la
    forme [jour, mois, annee]
    """
    Moyenne=[3.7,4.4,8.1,11.7,15.6,20.2,22.6,22.1,18,13.6,8,4.5]
    Moyenne=RechauffementClimatique(Moyenne,Date)
    Mois=Date[1]-1 # On fait -1 car les dates commencent a 1
    Jour=Date[0]-1
    TempDepart=Moyenne[Mois]+uniform(-1,1) + choice([-1,1])*abs(1/(Mois-(randint(0,11)+uniform(0.1,0.9))))
    if Mois!=11:
        TempDepart=(TempDepart+(Moyenne[Mois+1]+uniform(-0.5,0.5)-TempDepart)*Jour/31)
    else:
        TempDepart=(TempDepart+(Moyenne[0]+uniform(-0.5,0.5)-TempDepart)*Jour/31)
        
    return TempDepart

def DrawStadiumExample(nbX, nbY):
    """
    Renvoie le visuel de la repartition des capteurs du stade selon
    leur nombre nbX et nbY qui correspondent au nombre de capteurs sur
    x et y
    """

    imageData = gaussian_filter(
        [[(0,(40 + randint(1, 10))*7,0) for _ in range(100)] for _ in range(50)],
        sigma=0.75)

    for i in range(int(25//nbY), 50, int(50//nbY)):
        for j in range(int(50//nbX), 100, int(100//nbX)):
            imageData[i][j] = (255, 0, 0)

    finalImage = np.array(imageData).astype(np.uint8)

    matim.imsave("./src/temp/tempGraph.png", finalImage)        
    image = Image.open("./src/temp/tempGraph.png")        
    image = image.resize((500, 250))        
    photo = ImageTk.PhotoImage(image)        
    return photo

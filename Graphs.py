from matplotlib import pyplot as plt
from PIL import Image, ImageTk
import numpy as np
from scipy.ndimage import gaussian_filter
from random import randint, uniform
from matplotlib import image as matim
import math

def CreateDayTemp(heure, dayMedium)->int:
    # Technique de l'autruche: les chances que daymedium == 0
    # sont tellement faibles qu'on va ignorer le bug au lieu de le fix
    #print(heure, dayMedium)
    rep = dayMedium-2 + np.sin(heure*np.pi/12 +dayMedium/6 +1)*6
    
    return rep

def RechauffementClimatique(Moyenne,Date):   
    if Date[2]>2000:
        for k in range(len(Moyenne)):
            Moyenne[k]+=math.log(Moyenne[k]/3*(Date[2]-2000),2.7)
    print("pn est la")
    return Moyenne
                    
def CreateTemp(Date):
    Moyenne=[3.7,4.4,8.1,11.7,15.6,20.2,22.6,22.1,18,13.6,8,4.5]
    print("zaefdgn,;")
    Moyenne=RechauffementClimatique(Moyenne,Date)
    Mois=Date[1]-1 # On fait -1 car les dates commencent a 1
    Jour=Date[0]-1
    TempDepart=Moyenne[Mois]+uniform(-0.4,0.4)
    if Mois!=11:
        TempDepart=TempDepart+(Moyenne[Mois+1]+uniform(-0.2,0.2)-TempDepart)*Jour/31
    return TempDepart

def DrawStadiumExample(nbX, nbY):

    imageData = gaussian_filter([[(0,(40 + randint(1, 10))*7,0) for _ in range(100)] for _ in range(50)], sigma=0.75)

    for i in range(int(25/nbY), 50, int(50/nbY+1)-1):
        for j in range(int(50//nbX), 100, int(100//nbX)):
            imageData[i][j] = (255, 0, 0)

    finalImage = np.array(imageData).astype(np.uint8)

    #print(finalImage)

    matim.imsave("./temp/tempGraph.png", finalImage)        
    image = Image.open("./temp/tempGraph.png")        
    image = image.resize((500, 250))        
    photo = ImageTk.PhotoImage(image)        
    return photo
    
if __name__ == "__main__":

    print(DrawStadiumExample(100, 50))
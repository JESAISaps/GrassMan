from matplotlib import pyplot as plt
from PIL import Image, ImageTk
import numpy as np
from scipy.ndimage import gaussian_filter
from random import randint
from matplotlib import image as matim

def CreateTemp(heure, dayMedium)->int:
    # Technique de l'autruche: les chances que daymedium == 0
    # son tellement faibles qu'on va ignorer le bug au lieu de le fix
    #print(heure, dayMedium)
    return dayMedium - ((heure - 12)**2)/dayMedium

def DrawStadiumExample(nbX, nbY):
    blankArray = [[0]*100 for _ in range(50)]
    imageData = [[[0,(zero + randint(1, 20))*7,0] for zero in ligne] for ligne in blankArray]

    for i in np.arange(1, nbX, 50/nbY):
        for j in np.arange(1, nbY, 100/nbX):
            imageData[int(i)][int(j)] = (254, 0, 0) 
    print(imageData)
    finalImage = np.array(gaussian_filter(imageData, sigma=0.75)).astype(np.uint8)

    matim.imsave("./temp/tempGraph.png", finalImage)        
    image = Image.open("./temp/tempGraph.png")        
    image = image.resize((500, 250))        
    photo = ImageTk.PhotoImage(image)        
    return photo
    
    

#def DrawGraph(temps:list[tuple]):
#    """
#    Draws a graph from points in tuple:
#    temps must be [(hour, temp)] and len(temps) <= 24
#    """
#    #plt.clf()
#    plt.plot(temps)
#    plt.savefig("./temp/tempGraph.png")
#    image = Image.open("./temp/tempGraph.png").resize((500, 250))
#    photo = ImageTk.PhotoImage(image)
#    return photo
#
#def GetGraph(medium):
#    hourlyTemp = []
#    for heure in range(24):
#        hourlyTemp.append(CreateTemp(heure, medium))
#    return DrawGraph(hourlyTemp)
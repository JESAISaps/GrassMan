from matplotlib import pyplot as plt
from PIL import Image, ImageTk
import numpy as np
from scipy.ndimage import gaussian_filter
from random import randint
from matplotlib import image as matim

def CreateTemp(heure, dayMedium)->int:
    # Technique de l'autruche: les chances que daymedium == 0
    # sont tellement faibles qu'on va ignorer le bug au lieu de le fix
    #print(heure, dayMedium)
    return dayMedium - ((heure - 12)**2)/dayMedium

def DrawStadiumExample(nbX, nbY):

    imageData = [[(0,(40 + randint(1, 10))*7,0) for _ in range(100)] for _ in range(50)]

    for i in range(1, nbY+1, 50//nbY):
        for j in range(1, nbX+1, 100//nbX):
            imageData[i][j] = (200, 0, 0)
    #print(imageData)
    finalImage = np.array(gaussian_filter(imageData, sigma=0.75)).astype(np.uint8)

    #print(finalImage)

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
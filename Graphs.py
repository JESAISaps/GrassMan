import matplotlib
from matplotlib import pyplot as plt
from PIL import Image, ImageTk

def CreateTemp(heure, dayMedium)->int:
    # Technique de l'autruche: les chances que daymedium == 0
    # son tellement faibles qu'on va ignorer le bug au lieu de le fix
    #print(heure, dayMedium)
    return dayMedium - ((heure - 12)**2)/dayMedium

def DrawGraph(temps:list[tuple]):
    """
    Draws a graph from points in tuple:
    temps must be [(hour, temp)] and len(temps) <= 24
    """
    #plt.clf()
    plt.plot(temps)
    plt.savefig("./temp/tempGraph.png")
    image = Image.open("./temp/tempGraph.png").resize((500, 250))
    photo = ImageTk.PhotoImage(image)
    return photo

def GetGraph(medium):
    hourlyTemp = []
    for heure in range(24):
        hourlyTemp.append(CreateTemp(heure, medium))
    return DrawGraph(hourlyTemp)
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

# Créer une figure et un premier jeu d'axes
fig = Figure(figsize=(6.8,4.2), dpi=100)
ax1 = fig.add_subplot(111)

# Ajouter un premier graphique à gauche
ax1.plot([1, 2, 3, 4], [1, 4, 2, 3], 'b-')
ax1.set_xlabel('X axis')
ax1.set_ylabel('Y axis (left)', color='b')

# Créer un deuxième jeu d'axes qui partage l'axe des abscisses
ax2 = ax1.twinx()

# Ajouter un deuxième graphique à droite
ax2.plot([1, 2, 3, 4], [5, 2, 3, 1], 'r-')
ax2.set_ylabel('Y axis (right)', color='r')

# Afficher la figure

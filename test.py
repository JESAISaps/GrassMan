import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# Créer une fenêtre Tkinter
window = tk.Tk()
window.title("Matplotlib dans Tkinter")

# Créer une figure Matplotlib et un canvas Tkinter associé
figure = Figure(figsize=(5, 4), dpi=100)
canvas = FigureCanvasTkAgg(figure, master=window)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Créer un graphique Matplotlib dans la figure
axes = figure.add_subplot(111)
x = np.linspace(0, 10, 100)
y = np.sin(x)
axes.plot(x, y)
axes.set_xlabel("x")
axes.set_ylabel("sin(x)")
axes.set_title("Graphique de sin(x)")

# Lancer la boucle principale Tkinter
window.mainloop()
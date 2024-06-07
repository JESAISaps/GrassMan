import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from tkscrolledframe import ScrolledFrame
import tkcalendar
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates
from matplotlib.colors import TABLEAU_COLORS

from datetime import datetime, timedelta, date
from calendar import monthrange, isleap
from math import sqrt

from Stades import Stade
import numpy as np
import sqlite3
import BDDapi
import Graphs

from colors import GREEN, GREY

class StadiumFrameTemplate(tk.Frame):
    """
    Main stadium window with graphs
    """
    def __init__(self, parent:tk.Frame, root, nomStade:str, dimentions):
        root.update_idletasks()
        # initialises Frame
        tk.Frame.__init__(self, parent, width=root.winfo_width()-root.winfo_width()//5, height=root.winfo_height(), highlightbackground="black", highlightthickness=1)
        self.root = root
        self.name = nomStade

        self.stadiumNameFrame = tk.Frame(self)
        self.graphFrame = tk.Frame(self, highlightbackground="black", highlightthickness=1)
        self.configureStadiumFrame = tk.Frame(self, highlightbackground="black", highlightthickness=1)

        def GetBoolStateString(state):
            """
            Transform un bool en son equivalent francais
            """
            if state:
                return "On"
            return "Off"
        
        self.isHeating = tk.BooleanVar(value=False)
        self.heatingLabel = ttk.Label(self.configureStadiumFrame, text="Chauffage : " + GetBoolStateString(self.isHeating.get()))
        self.heatingButton = ttk.Button(self.configureStadiumFrame, text="Allumer / Eteindre", command= lambda : (self.isHeating.set( not self.isHeating.get()),
                                                                                                        self.heatingLabel.configure(text="Chauffage : " + GetBoolStateString(self.isHeating.get()))))
                                                                                                        #, self.update_idletasks()))
        
        self.arrosage = tk.BooleanVar(value=False)
        self.arrosageLabel = ttk.Label(self.configureStadiumFrame, text="Arrosage : " + GetBoolStateString(self.arrosage.get()))
        self.arrosageButton = ttk.Button(self.configureStadiumFrame, text="Allumer / Eteindre", command= lambda : (self.arrosage.set( not self.arrosage.get()),
                                                                                                        self.arrosageLabel.configure(text="Arrosage : " + GetBoolStateString(self.arrosage.get()))))
                                                                                                        #, self.update_idletasks()))        
        
        self.showSeuil = tk.BooleanVar(value=False)
        self.showSeuilLabel = ttk.Label(self.configureStadiumFrame, text="Seuils : " + GetBoolStateString(self.showSeuil.get()))
        self.showSeuilButton = ttk.Button(self.configureStadiumFrame, text="Montrer / Cacher", command= lambda : (self.showSeuil.set(not self.showSeuil.get()),
                                                                                                            self.showSeuilLabel.configure(text="Seuils : " + GetBoolStateString(self.showSeuil.get()))))

        self.dimText = f"   Capteurs \nLongueur: {dimentions[0]}\nLargeur: {dimentions[1]}"
        self.repartitionCapteursLabel = ttk.Label(self.configureStadiumFrame, text = self.dimText)
        
        self.isHeating.trace_add("write", lambda e,a,z: self.UpdateGraph())
        self.arrosage.trace_add("write",lambda e,a,z: self.UpdateGraph())
        self.showSeuil.trace_add("write", lambda e,a,z: self.UpdateGraph())

        self.repartitionCapteursLabel.pack(side="top", pady=(3, 0), padx=20)

        self.stadiumNameLabel = ttk.Label(self.stadiumNameFrame, text=self.name, font="Bold 30")

        self.showTodayBool = tk.BooleanVar(value=False)
        self.showToday = ttk.Checkbutton(self.graphFrame, text="Aujourd'hui", variable=self.showTodayBool, command= lambda : self.UpdateGraph(True))
        
        self.graph = Figure(figsize=(6.8,4.2), dpi=100)
        self.calendar = tkcalendar.Calendar(self, locale="fr",day= (datetime.today() - timedelta(days=1)).day, maxdate=datetime.today() - timedelta(days=1),
                                            mindate=datetime(2000, 1, 1), background=GREY, selectbackground = GREEN, font="Arial 12", foreground="black")
        self.calendar.selection_set(datetime.today() - timedelta(1))
        self.graphCanvas = FigureCanvasTkAgg(self.graph, master=self.graphFrame)
        self.graphCanvas.draw()

        self.modeChoice = tk.StringVar()
        self.modeSelection = ttk.Combobox(self.graphFrame, values=["Jour", "Mois", "Année"], textvariable=self.modeChoice, state="readonly")
        self.modeSelection.current(0)
        self.modeChoice.trace_add("write", lambda e,a,z: self.UpdateGraph())
        #create the stadium we'll get data from
        self.stade = Stade(nomStade, dimentions)
        self.calendar.bind("<<CalendarSelected>>", lambda e: self.UpdateGraph())

        #region InfoCapteurs

        self.capteurInfoFrame = ScrolledFrame(self, width = 500, height = 200, scrollbars = "vertical", use_ttk = True)        
        self.capteurInfoFrame.bind_arrow_keys(self.root)
        self.capteurInfoFrame.bind_scroll_wheel(self.root)

        self.displayCapteur = self.capteurInfoFrame.display_widget(tk.Frame)
        self.capteurs:list[tk.Button] = []
        nbCapteurs = self.stade.GetSize()
        for i in range(nbCapteurs[0]):
            for j in range(nbCapteurs[1]):
                self.capteurs.append(ttk.Label(self.displayCapteur, text= f"Capteur {str(i+j)} : {0}°C"))

        #endregion

        self.heatingLabel.pack(side="top")
        self.heatingButton.pack(side="top")
        self.arrosageLabel.pack(side="top", pady=(10, 0))
        self.arrosageButton.pack(side="top", pady=(0, 10))

        self.stadiumNameLabel.pack()
        self.repartitionCapteursLabel.pack()

        self.graphCanvas.get_tk_widget().pack(anchor="e")
        self.modeSelection.pack(side="left", padx=(5), pady=2)
        self.showToday.pack(side="right", padx=(5), pady=2)

        self.capteurInfoFrame.grid(column=1, row=5, columnspan=4, rowspan=3, padx=20, pady=30)
        self.graphFrame.grid(column=1, row=0, columnspan=5, rowspan=3, padx=(0,10), pady=(10, 0))
        self.calendar.grid(column=5, row=4, padx=(0,10), pady=(10, 10), sticky = "E")
        self.stadiumNameFrame.grid(column=2, row=4, pady=30)
        self.configureStadiumFrame.grid(column=0, row=1, padx=(10,10), pady=(10, 0))

        self.pack_propagate(False)
        self.grid_propagate(False)


        self.ToggleTodayGraph(self.showTodayBool.get())

    def ToggleTodayGraph(self, state):
        """
        passe de l'affichage du jour aux archives
        """
        if state: # If we only want to show today's temps
            self.calendar.grid_remove()
            self.stadiumNameFrame.grid_remove()
            self.modeSelection.pack_forget()
            self.capteurInfoFrame.grid()
            self.showSeuilLabel.pack(side="top", pady=(10, 0))
            self.showSeuilButton.pack(side="top")
            self.heatingLabel.pack(side="top", pady=(7, 0))
            self.heatingButton.pack(side="top")
            self.arrosageLabel.pack(side="top", pady=(10, 0))
            self.arrosageButton.pack(side="top")
        else:
            self.capteurInfoFrame.grid_remove()
            self.stadiumNameFrame.grid()
            self.calendar.grid()
            self.modeSelection.pack(side="left", padx=(5), pady=2)            
            self.showSeuilLabel.pack_forget()
            self.showSeuilButton.pack_forget()
            self.heatingLabel.pack_forget()
            self.heatingButton.pack_forget()
            self.arrosageLabel.pack_forget()
            self.arrosageButton.pack_forget()

    def UpdateGraph(self, isToggling=False):
        """
        Refreshes graph
        """
        # cette ligne est trop belle pour etre enlevée
        #imageData = np.array(gaussian_filter([[[0,(element+20)*7,0] for element in ligne] for ligne in data], sigma=0.75)).astype(np.uint8)
        
        try:
            self.graph.clf()
        except:
            return
        if isToggling:
            self.ToggleTodayGraph(self.showTodayBool.get())

        self.axes = self.graph.add_subplot(111)
        isPredicting = (False, 24)        
        xLabel = ""
        isYear = False
        if(self.showTodayBool.get()):            

            nbValeurs = np.arange(datetime.now().hour + 1)
            bdd = sqlite3.connect(self.root.BDDPATH)
            dayMedium = BDDapi.GetMediumTemp(bdd, self.name, datetime.now().date())
            temps = np.array([Graphs.CreateDayTemp(hour, dayMedium) for hour in nbValeurs])


            isPredicting = (True, nbValeurs.size-1)
            for hour in range(nbValeurs.size, 24):
                nbValeurs = np.append(nbValeurs, hour)
                temps = np.append(temps, Graphs.CreateDayTemp(hour, dayMedium+ 7*self.isHeating.get() - 5*self.arrosage.get()))
            bdd.close()
            
            self.axes.set_title("Températures du jour")
        else:
            match self.modeSelection.get():
                case "Jour":
                    nbValeurs = np.arange(24)
                    bdd = sqlite3.connect(self.root.BDDPATH)
                    dayMedium = BDDapi.GetMediumTemp(bdd, self.name, self.calendar.selection_get())
                    temps = np.array([Graphs.CreateDayTemp(hour, dayMedium) for hour in nbValeurs])
                    precip = np.array([Graphs.CreateDayPrecip(hour, self.calendar.selection_get().day,self.calendar.selection_get().month,dayMedium) for hour in nbValeurs])
                    precax=self.axes.twinx()
                    precax.set_ylim(0, 100)
                    precax.set_ylabel("Précipitations (mm)", color="green")
                    precax.plot(nbValeurs, precip,"C2", label="Précipitations")
                    xLabel = "Heure"                    
                    self.axes.set_title("Températures de la journée")
                    self.axes.plot(nbValeurs, temps, label="Mesures Températures")
                    precax.legend(loc="upper left")
                    bdd.close()

                case "Mois":
                    bdd = sqlite3.connect(self.root.BDDPATH)
                    nbValeurs = np.arange(monthrange(*self.calendar.get_displayed_month()[::-1])[1])            
                    temps = np.array(BDDapi.GetTempsInMonth(bdd, self.name, *self.calendar.get_displayed_month()))
                    xLabel = "Jour"
                    self.axes.set_title("Températures du mois")
                    
                    if self.calendar.selection_get().year == datetime.now().year and self.calendar.selection_get().month == datetime.now().month:
                        whereToCut = datetime.now().day - 1
                        self.axes.plot(nbValeurs[:whereToCut+1], temps[:whereToCut+1], label="Mesures Températures")
                        self.axes.plot(nbValeurs[whereToCut:], temps[whereToCut:], "g--", label="Prédictions Températures")
                    else:
                        self.axes.plot(nbValeurs, temps)
                    
                    aimedDayIndex = abs(date(self.calendar.selection_get().year, self.calendar.selection_get().month, 1) - self.calendar.selection_get()).days
                    self.axes.plot(nbValeurs[aimedDayIndex], temps[aimedDayIndex], "ro")

                    bdd.close()

                case "Année":
                    bdd = sqlite3.connect(self.root.BDDPATH)
                    nbValeurs = np.arange(365 + isleap(self.calendar.selection_get().year))
                    temps = np.array(BDDapi.GetTempsInYear(bdd, self.name, self.calendar.get_displayed_month()[1]))
                    xLabel = "Jour"
                    self.axes.set_title("Températures de l'année")

                    firstDay = datetime(self.calendar.selection_get().year, 1, 1)
                    dates = np.array([firstDay + timedelta(days=day.item()) for day in nbValeurs])
                    
                    if self.calendar.selection_get().year == datetime.now().year:
                        whereToCut = abs(date(self.calendar.selection_get().year, 1, 1) - date.today()).days
                        self.axes.plot(dates[:whereToCut+1], temps[:whereToCut+1], label="Mesures Températures")
                        self.axes.plot(dates[whereToCut:], temps[whereToCut:], "g--", label="Prédictions Températures")
                    else:
                        self.axes.plot(dates, temps)
                    isYear = True
                    aimedDayIndex = abs(date(self.calendar.selection_get().year, 1, 1) - self.calendar.selection_get()).days
                    self.axes.plot(dates[aimedDayIndex], temps[aimedDayIndex], "ro")
                    bdd.close()
                case _:
                    print("Ho no")

        if isPredicting[0]:
            self.axes.plot(nbValeurs[:isPredicting[1]], temps[:isPredicting[1]], label="Mesures Températures", linewidth=2)
            self.axes.plot(nbValeurs[isPredicting[1]-1:], temps[isPredicting[1]-1:], "g--", label="Prédictions Températures", linewidth=2)

            if self.showSeuil.get():
                self.axes.plot(nbValeurs, [25]*len(nbValeurs), "r-.", linewidth=.5)
                self.axes.plot(nbValeurs, [5]*len(nbValeurs), "r-.", linewidth=.5)

            # On crée d'autres temperatures pour faire croire que tous les capteurs marchent
            # Plus il y a de capteurs plus les temperatures sont proches
            for i, element in enumerate(self.capteurs):
                element.configure(text=f"Capteur {i+1} : {Graphs.CreateDayTemp(datetime.now().hour, dayMedium)- sqrt((i//5)**2 + (i%5)**2)* 0.07:.2f}°C")
                element.grid(row=i//5, column=i%5, padx=2, pady=2)
                element.update_idletasks()
            
        leg = self.axes.legend(loc="upper right")
        for line in leg.get_lines():
            line.set_linewidth(2)

        if not isYear:
            self.axes.set_xlim(1, max(len(nbValeurs)-1, 23))
        self.axes.set_ylim(-5, 35)
        self.axes.set_xlabel(xLabel)
        self.axes.set_ylabel("Températures (C°)", color=TABLEAU_COLORS["tab:blue"])

        if isYear:
            self.axes.xaxis_date()
            self.axes.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
            self.axes.xaxis.set_major_locator(mdates.MonthLocator())

            labels = self.axes.xaxis.get_ticklabels()
            for label in labels:
                label.set_rotation(45)
        self.graphCanvas.draw()

        #self.update_idletasks()

    def createNewTempFromDefault(self, oldtemps):
        """
        met de l'aleatoire dans les temperatures des capteurs, mais bien fait,
        et de maniere uniforme.
        """
        rep = []
        if oldtemps[0]%2 == 1:
            sign = 1
        else:
            sign = -1

        toAdd = int(str((oldtemps[0]**2)*sign)[:3])/200
        for temp in oldtemps:
            rep.append(temp + toAdd)
        return np.array(rep)


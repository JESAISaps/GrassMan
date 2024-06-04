class Stade:
    """
    Object which contains informations about stadium displayed in StadiumFrameTemplate
    """
    def __init__(self, nom:str, dimensions) -> None:
        self.nom = nom
        self.longueur = dimensions[0]
        self.largeur = dimensions[1]

        self.capteurs = [[(i, j) for j in range(dimensions[0]) for i in range(dimensions[1])]]

    def GetSize(self):
        """
        retourne la variable taille du stade sous la forme d'un tuple
        """
        return self.longueur, self.largeur
          
    def GetIdStade(self):
        return self.nom


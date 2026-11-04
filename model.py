# models.py
# Ici, on décrit ce qu'est un combattant et une équipe.

# Constante : un coup qui touche fait toujours au moins 1 dégât
DEGATS_MINIMUM = 1


# Une classe = un plan de fabrication.
# Ici, le plan d'un combattant (personnage OU monstre, ils ont les mêmes stats).
class Combattant:

    # __init__ se lance automatiquement quand on fabrique un combattant.
    # "self" veut dire "ce combattant-là".
    def __init__(self, nom, attaque, defense, pv):
        self.nom = nom
        self.attaque = int(attaque)   # int() = on force un nombre entier
        self.defense = int(defense)
        self.pv_max = int(pv)         # les PV de départ
        self.pv = self.pv_max         # les PV actuels (au début = le max)

    # Fabrique un combattant à partir d'un dictionnaire venant de MongoDB
    @classmethod
    def depuis_dict(cls, data):
        return cls(data["nom"], data["attaque"], data["defense"], data["pv"])

    # Renvoie True si le combattant a encore des PV
    def est_vivant(self):
        return self.pv > 0

    # Le combattant reçoit un coup
    def recevoir_degats(self, degats_bruts):
        # Dégâts = force du coup - ma défense (mais jamais moins que 1)
        degats = max(DEGATS_MINIMUM, degats_bruts - self.defense)
        # On enlève les dégâts aux PV (sans descendre sous 0)
        self.pv = max(0, self.pv - degats)
        return degats

    # Le combattant attaque une cible
    def attaquer(self, cible):
        return cible.recevoir_degats(self.attaque)

    # Texte affiché quand on fait print(combattant)
    def __str__(self):
        return (f"{self.nom} | ATK: {self.attaque} | DEF: {self.defense} "
                f"| PV: {self.pv}/{self.pv_max}")


# Personnage et Monstre "héritent" de Combattant :
# ils ont tout ce que Combattant sait faire, sans le réécrire.
class Personnage(Combattant):
    pass  # "pass" = rien à ajouter


class Monstre(Combattant):
    pass


# Une équipe = une liste de personnages
class Equipe:

    def __init__(self):
        self.personnages = []  # liste vide au départ

    # Ajoute un personnage à la fin de la liste
    def ajouter(self, personnage):
        self.personnages.append(personnage)

    # Retire le dernier personnage ajouté (ou renvoie None s'il n'y en a pas)
    def retirer_dernier(self):
        return self.personnages.pop() if self.personnages else None

    # True si au moins un personnage est encore vivant
    def est_en_vie(self):
        return any(p.est_vivant() for p in self.personnages)

    # Renvoie seulement les personnages vivants
    def membres_vivants(self):
        return [p for p in self.personnages if p.est_vivant()]

    # Permet d'écrire len(equipe) pour connaître le nombre de membres
    def __len__(self):
        return len(self.personnages)

    # Texte affiché quand on fait print(equipe)
    def __str__(self):
        lignes = []
        for i, p in enumerate(self.personnages, 1):
            statut = "" if p.est_vivant() else " [K.O.]"
            lignes.append(f"  {i}. {p}{statut}")
        return "\n".join(lignes)
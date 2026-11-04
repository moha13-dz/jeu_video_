# affichage.py
# Le seul fichier qui affiche des choses à l'écran (print).
# Il ne parle pas à MongoDB : on lui donne les données, il les affiche.

from config import LIGNE, LONGUEUR_MAX_NOM, SEPARATEUR


# Dessine une barre de vie, par exemple : ████░░░░░░
def barre_pv(pv, pv_max, largeur=10):
    # Nombre de carrés pleins = PV restants / PV max, sur 10 carrés
    rempli = round(largeur * pv / pv_max) if pv_max else 0
    # S'il reste des PV, on affiche au moins 1 carré plein
    if pv > 0:
        rempli = max(1, rempli)
    # "█" = carré plein, "░" = carré vide
    return "█" * rempli + "░" * (largeur - rempli)


# Une ligne qui résume l'état d'un combattant (personnage ou monstre)
def ligne_combattant(c):
    ko = "  💀" if not c.est_vivant() else ""
    # :<11 = on aligne à gauche sur 11 caractères, :>3 = à droite sur 3
    return (f"{c.nom:<11} {barre_pv(c.pv, c.pv_max)} {c.pv:>3}/{c.pv_max:<3} "
            f"ATK {c.attaque:>2}  DEF {c.defense:>2}{ko}")


# Affiche le titre du jeu
def afficher_titre():
    print("\n" + SEPARATEUR)
    print("          ⚔️   JEU DE COMBAT PAR VAGUES   ⚔️")
    print(SEPARATEUR)


# Affiche le menu principal
def afficher_menu():
    afficher_titre()
    print("  1. Démarrer le jeu")
    print("  2. Afficher le classement")
    print("  3. Quitter")
    print(SEPARATEUR)


# Affiche le classement. On lui donne la liste des scores en paramètre.
def afficher_classement(classement):
    print("\n" + SEPARATEUR)
    print("            🏆  MEILLEURS SCORES  🏆")
    print(SEPARATEUR)
    if not classement:
        print("  Aucun score enregistré pour le moment.")
    else:
        medailles = ["🥇", "🥈", "🥉"]
        for i, entree in enumerate(classement):
            vagues = entree["vagues"]
            # On met un "s" à "vague" seulement s'il y en a plus d'une
            print(f"  {medailles[i]}  {entree['joueur']:<{LONGUEUR_MAX_NOM}} "
                  f"{vagues} vague{'s' if vagues > 1 else ''}")
    print(SEPARATEUR + "\n")


# Affiche la liste des personnages disponibles
def afficher_liste_personnages(personnages, deja_choisis=()):
    print("\n" + LIGNE)
    print("  PERSONNAGES DISPONIBLES")
    print(LIGNE)
    for i, p in enumerate(personnages, 1):
        # Si le personnage est déjà dans l'équipe, on ajoute "✔ choisi"
        marque = "  ✔ choisi" if p["nom"] in deja_choisis else ""
        print(f"  {i:>2}. {p['nom']:<12} ATK: {p['attaque']:>2}  "
              f"DEF: {p['defense']:>2}  PV: {p['pv']:>3}{marque}")
    print(LIGNE)


# Affiche l'équipe en cours de création
def afficher_equipe_creation(equipe):
    print("\n  📋 Équipe actuelle :")
    if not equipe.personnages:
        print("     (vide)")
        return  # on s'arrête ici si l'équipe est vide
    for i, p in enumerate(equipe.personnages, 1):
        print(f"     Personnage numero {i} - {p.nom} - {p.attaque} ATK - {p.defense} DEF - {p.pv_max} PV")
# ── Affichage pour la partie (utilisé par game.py) ──

# Affiche simplement un texte
def afficher_message(texte):
    print(texte)


# Affiche l'équipe finale avant validation
def afficher_equipe_finale(equipe):
    print("\n" + SEPARATEUR)
    print("    Équipe finale :")
    afficher_equipe_creation(equipe)
    print(SEPARATEUR)


# Affiche le début d'une vague : le monstre et l'équipe
def afficher_debut_vague(equipe, monstre, vague):
    print(f"\n{SEPARATEUR}")
    print(f"   VAGUE {vague}")
    print(SEPARATEUR)
    print("   Un monstre apparaît !")
    print(f"     {monstre}")
    print(LIGNE)
    print("  s  Ton équipe :")
    for p in equipe.personnages:
        print(f"     {ligne_combattant(p)}")
    print(LIGNE)


# Affiche le numéro du tour
def afficher_tour(tour):
    print(f"\n  ── Tour {tour} ──")


# Affiche l'attaque d'un personnage sur le monstre
def afficher_attaque_perso(perso, monstre, degats):
    print(f"  🗡️  {perso.nom:<10} → {monstre.nom}  -{degats:<3} "
          f"{barre_pv(monstre.pv, monstre.pv_max)} {monstre.pv}/{monstre.pv_max}")


# Affiche l'attaque du monstre sur un personnage
def afficher_attaque_monstre(monstre, cible, degats):
    print(f"  💥  {monstre.nom} → {cible.nom:<10} -{degats:<3} "
          f"{barre_pv(cible.pv, cible.pv_max)} {cible.pv}/{cible.pv_max}")
    if not cible.est_vivant():
        print(f"  💀  {cible.nom} est hors combat !")


# Affiche le résultat d'un combat (victoire ou défaite)
def afficher_fin_combat(monstre, tour, victoire):
    if victoire:
        print(f"\n  🎉 Victoire en {tour} tour(s) ! {monstre.nom} est vaincu !")
    else:
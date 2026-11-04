# saisie.py
# Le seul fichier qui pose des questions au joueur (input)
# et qui vérifie ses réponses.

from config import LONGUEUR_MAX_NOM


# Demande un nombre entier entre min_val et max_val
def saisir_entier(message, min_val, max_val):
    # "while True" = on répète sans arrêt, jusqu'à ce qu'on fasse "return"
    while True:
        # input() lit ce que le joueur tape, strip() enlève les espaces autour
        saisie = input(message).strip()
        try:
            # On essaie de transformer le texte en nombre
            valeur = int(saisie)
        except ValueError:
            # Si ce n'est pas un nombre (ex : "abc"), on prévient et on recommence
            print("  ⚠️  Entrée invalide. Veuillez entrer un nombre entier.")
            continue  # retour au début de la boucle
        # Le nombre est-il entre le minimum et le maximum ?
        if min_val <= valeur <= max_val:
            return valeur  # oui : on renvoie le nombre et on sort
        print(f"  ⚠️  Entrez un nombre entre {min_val} et {max_val}.")


# Pose une question oui/non. Renvoie True pour oui, False pour non.
def saisir_oui_non(message):
    while True:
        # lower() = tout en minuscules, pour accepter "O", "Oui", "OUI"...
        reponse = input(message).strip().lower()
        if reponse in ("o", "oui", "y", "yes"):
            return True
        if reponse in ("n", "non", "no"):
            return False
        print("  ⚠️  Réponds par 'o' (oui) ou 'n' (non).")


# Demande le nom du joueur (pas vide, 20 caractères maximum)
def saisir_nom():
    while True:
        # split() découpe en mots, " ".join(...) les recolle avec un seul espace
        # Ça enlève les espaces en trop
        nom = " ".join(input("  Votre nom d'utilisateur : ").split())
        if not nom:
            print("  ⚠️  Le nom ne peut pas être vide.")
        elif len(nom) > LONGUEUR_MAX_NOM:
            print(f"  ⚠️  Le nom ne peut pas dépasser {LONGUEUR_MAX_NOM} caractères.")
        elif not nom.isprintable():
            # isprintable() est False s'il y a des caractères invisibles
            print("  ⚠️  Le nom contient des caractères invalides.")
        else:
            return nom  # le nom est bon : on le renvoie
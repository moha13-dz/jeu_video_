# main.py
# Le point de départ du jeu. Pour jouer : python main.py

import sys  # sert à quitter le programme avec un code (0 = OK, 1 = erreur)

from pymongo.errors import PyMongoError  # erreur possible venant de MongoDB

from affichage import afficher_classement, afficher_menu, afficher_message
from database import BaseDeDonnees, ErreurBase
from game import lancer_partie
from saisie import saisir_entier, saisir_nom


def main():
    # On crée la connexion à MongoDB UNE SEULE FOIS ici.
    # Ensuite, on la donne (en paramètre) aux fonctions qui en ont besoin.
    base = BaseDeDonnees()

    code = 0  # 0 = tout s'est bien passé

    try:
        # On vérifie que MongoDB est lancé et que la base est remplie
        base.verifier()

        # La boucle du menu : elle revient tant que le joueur ne quitte pas
        while True:
            afficher_menu()
            choix = saisir_entier("  Ton choix : ", 1, 3)

            if choix == 1:
                nom = saisir_nom()                       # on demande le nom
                lancer_partie(base, nom)                 # on lance la partie
                afficher_classement(base.get_classement())  # puis le classement
            elif choix == 2:
                afficher_classement(base.get_classement())
            else:
                break  # choix 3 : on sort de la boucle, donc on quitte

    except (KeyboardInterrupt, EOFError):
        # Le joueur a fait Ctrl+C ou Ctrl+D : ce n'est pas une vraie erreur
        afficher_message("")

        

    except ErreurBase as exc:
        # Notre erreur personnalisée (MongoDB éteint, base vide...)
        afficher_message(f"\n  ❌  {exc}\n")
        code = 1

    except PyMongoError as exc:
        # Une erreur venant directement de MongoDB
        afficher_message(f"\n   Erreur MongoDB : {exc}\n")
        code = 1

    finally:
        # "finally" s'exécute TOUJOURS, même après une erreur :
        # on ferme la connexion pour ne rien laisser ouvert
        base.fermer()

    afficher_message("\n  À bientôt ! 👋\n")
    return code


# Veut dire : "lance main() seulement si on a lancé CE fichier directement"
if __name__ == "__main__":
    sys.exit(main())
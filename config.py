# config.py
# Ici, on met tous les réglages du jeu.

# Où se trouve MongoDB sur ton ordinateur
MONGO_URI = "mongodb://localhost:27017/"

# Le nom de notre base de données
DB_NAME = "jeu_video"

# Combien de scores on garde dans le classement
NB_MEILLEURS_SCORES = 3

# Nombre maximum de lettres pour le nom du joueur
LONGUEUR_MAX_NOM = 20

# Deux lignes de décoration pour faire joli à l'écran
SEPARATEUR = "═" * 50
LIGNE = "─" * 50
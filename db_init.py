# db_init.py
# Remplit MongoDB avec les personnages et les monstres.
#
#   python db_init.py            → ajoute / met à jour (les scores sont gardés)
#   python db_init.py --reset    → repart de zéro (efface aussi les scores)

import argparse  # pour lire les options tapées dans le terminal (ex : --reset)
import json      # pour lire les fichiers .json
import sys
from pathlib import Path  # pour manipuler des chemins de fichiers

from pymongo import ASCENDING, DESCENDING, ReplaceOne
from pymongo.errors import PyMongoError

from config import DB_NAME, MONGO_URI
from database import BaseDeDonnees

# Le dossier "database" situé à côté de ce fichier
DOSSIER_DATA = Path(__file__).resolve().parent / "database"

# Les 3 "tables" (on dit des collections) de la base
COLLECTIONS = ("personnages", "monstres", "scores")

# Types de nombres entiers acceptés par MongoDB
ENTIER = ["int", "long"]

# Le "règlement" pour un personnage ou un monstre :
# MongoDB refusera tout document qui ne le respecte pas.
SCHEMA_STATS = {"$jsonSchema": {
    "bsonType": "object",
    "required": ["id", "nom", "attaque", "defense", "pv"],  # champs obligatoires
    "properties": {
        "id":      {"bsonType": ENTIER, "minimum": 1},
        "nom":     {"bsonType": "string"},
        "attaque": {"bsonType": ENTIER, "minimum": 0},
        "defense": {"bsonType": ENTIER, "minimum": 0},
        "pv":      {"bsonType": ENTIER, "minimum": 1},
    },
}}

# Le "règlement" pour un score
SCHEMA_SCORES = {"$jsonSchema": {
    "bsonType": "object",
    "required": ["joueur", "vagues", "date"],
    "properties": {
        "joueur": {"bsonType": "string", "minLength": 1},
        "vagues": {"bsonType": ENTIER, "minimum": 0},
        "date":   {"bsonType": "date"},
    },
}}


# Lit un fichier .json et renvoie son contenu sous forme de liste Python
def charger_json(nom_fichier):
    chemin = DOSSIER_DATA / nom_fichier
    #
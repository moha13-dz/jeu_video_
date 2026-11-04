# database.py
# Le seul fichier qui parle à MongoDB.
# Ici, aucun print() et aucun input().

from datetime import datetime, timezone  # pour enregistrer la date d'un score

from pymongo import ASCENDING, DESCENDING, MongoClient
from pymongo.errors import PyMongoError

from config import DB_NAME, MONGO_URI, NB_MEILLEURS_SCORES

# Constante : comment trier le classement
# (d'abord le plus de vagues, puis la date la plus ancienne si égalité)
TRI_CLASSEMENT = [("vagues", DESCENDING), ("date", ASCENDING)]


# Notre propre type d'erreur, pour les problèmes de base de données
class ErreurBase(Exception):
    pass


# Une classe qui représente la connexion à la base de données
class BaseDeDonnees:

    # Se lance quand on écrit BaseDeDonnees() : on crée la connexion
    def __init__(self):
        # self.client = la connexion, rangée DANS l'objet (pas en global)
        # Si MongoDB ne répond pas, on abandonne après 3 secondes
        self.client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=3000)
        self.db = self.client[DB_NAME]  # la base "jeu_video"

    # Ferme la connexion
    def fermer(self):
        self.client.close()

    # Vérifie que MongoDB est lancé et que la base est remplie
    def verifier(self):
        try:
            self.db.command("ping")  # "ping" = on demande : "tu es là ?"
            nb_persos = self.db.personnages.count_documents({})
            nb_monstres = self.db.monstres.count_documents({})
        except PyMongoError:
            raise ErreurBase(
                f"Impossible de joindre MongoDB ({MONGO_URI}).\n"
                "  → Vérifie que le serveur MongoDB est démarré."
            )
        if nb_persos < 3 or nb_monstres < 1:
            raise ErreurBase(
                "La base est vide ou incomplète.\n"
                "  → Lance d'abord :  python db_init.py"
            )

    # Renvoie tous les personnages, triés par id
    def get_tous_personnages(self):
        # {"_id": 0} = on cache le champ technique "_id"
        return list(self.db.personnages.find({}, {"_id": 0}).sort("id", ASCENDING))

    # Renvoie un monstre pioché au hasard
    def get_monstre_aleatoire(self):
        # "$sample" avec size 1 = MongoDB pioche 1 document au hasard
        resultats = list(self.db.monstres.aggregate(
            [{"$sample": {"size": 1}}, {"$project": {"_id": 0}}]
        ))
        if not resultats:
            raise ErreurBase("Aucun monstre en base. Lance d'abord : python db_init.py")
        return resultats[0]

    # Enregistre un score, garde seulement le top 3,
    # et renvoie le rang (1, 2 ou 3) ou None si pas dans le top
    def sauvegarder_score(self, nom_joueur, vagues):
        resultat = self.db.scores.insert_one({
            "joueur": nom_joueur,
            "vagues": vagues,
            "date": datetime.now(timezone.utc),
        })

        # On récupère tous les scores triés
        tous = list(self.db.scores.find({}, {"_id": 1}).sort(TRI_CLASSEMENT))

        # Tout ce qui dépasse le top 3 est supprimé
        a_supprimer = [doc["_id"] for doc in tous[NB_MEILLEURS_SCORES:]]
        if a_supprimer:
            self.db.scores.delete_many({"_id": {"$in": a_supprimer}})

        # Le score qu'on vient d'ajouter est-il dans le top 3 ? À quelle place ?
        for rang, doc in enumerate(tous[:NB_MEILLEURS_SCORES], 1):
            if doc["_id"] == resultat.inserted_id:
                return rang
        return None

    # Renvoie les 3 meilleurs scores
    def get_classement(self):
        return list(
            self.db.scores.find({}, {"_id": 0}).sort(TRI_CLASSEMENT).limit(NB_MEILLEURS_SCORES)
        )
# Trouver le nombre de pilotes totales dans la bdd

import redis
import json

# Connexion à la base de données Redis
r = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

def count_pilots():
    # Récupérer toutes les clés correspondant aux pilotes (par exemple, si elles commencent par 'PILOTE')
    pilote_keys = r.keys("PILOTE*")  # Assurez-vous que les clés des pilotes suivent un format unique, sinon changez "PILOTE*"
    
    # Si vos pilotes sont intégrés dans les informations de vol, nous les extrayons depuis les vols
    if not pilote_keys:
        print("Aucune clé de pilote séparée trouvée. Recherche dans les vols...")

        # Utiliser les vols pour extraire les pilotes uniques
        vol_keys = r.keys("V*")
        pilotes_set = set()

        for vol_key in vol_keys:
            vol_data = r.get(vol_key)
            if vol_data:
                vol_info = json.loads(vol_data)
                pilote = vol_info.get("pilote")
                if pilote:
                    # Ajoute le nom du pilote au set (pour éviter les doublons)
                    pilotes_set.add(pilote["NomPil"])
        
        # Afficher le nombre de pilotes uniques
        print(f"Nombre de pilotes uniques trouvés : {len(pilotes_set)}")
    else:
        # Si nous avons des clés de pilote séparées, afficher leur nombre
        print(f"Nombre de pilotes trouvés dans Redis : {len(pilote_keys)}")

# Exécution des fonctions
count_pilots() # Compte et affiche le nombre de pilotes
# Trouve la ville d'arrivé avec un numero de vol

import redis
import json

# Connexion à la base de données Redis
r = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

def get_ville_arrivee(num_vol):
    # Récupérer les informations du vol depuis Redis
    vol_data = r.get(num_vol)
    
    if vol_data:
        # Désérialiser la chaîne JSON pour obtenir un objet Python
        vol_info = json.loads(vol_data)
        
        # Extraire la ville d'arrivée
        ville_arrivee = vol_info.get("VilleA")
        
        if ville_arrivee:
            print(f"La ville d'arrivée pour le vol {num_vol} est : {ville_arrivee}")
        else:
            print(f"Aucune ville d'arrivée trouvée pour le vol {num_vol}.")
    else:
        print(f"Aucune donnée trouvée pour le vol {num_vol}.")

# Exécution pour un vol donné
num_vol = "V908"  # Remplacer par le numéro de vol réel
get_ville_arrivee(num_vol)


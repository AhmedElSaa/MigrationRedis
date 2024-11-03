# Trouve la ville d'arrivé avec un numero de vol

import redis   
import json    

# Connexion à la base de données Redis
r = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

def get_ville_arrivee(num_vol):

    # Récupérer les informations du vol
    vol_data = r.get(num_vol)
    
    if vol_data:
        # Désérialiser la chaîne JSON en dictionnaire
        vol_info = json.loads(vol_data)
        
        # Extraire la valeur associée à la clé 'VilleA', qui représente la ville d'arrivée
        ville_arrivee = vol_info.get("VilleA")
        
        # Vérifier si la ville d'arrivée est présente dans les données du vol
        if ville_arrivee:
            print(f"La ville d'arrivée pour le vol {num_vol} est : {ville_arrivee}")
        else:
            print(f"Aucune ville d'arrivée trouvée pour le vol {num_vol}.")
    else:
        print(f"Aucune donnée trouvée pour le vol {num_vol}.")

num_vol = "V117"
get_ville_arrivee(num_vol)

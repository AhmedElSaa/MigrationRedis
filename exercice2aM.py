# Trouver la ville d'arrivée avec un numéro de vol en utilisant MongoDB

from pymongo import MongoClient 

client = MongoClient('localhost', 27017)

# Sélection de la base de données
db = client['compagnie_aerienne']

def get_ville_arrivee(num_vol):
    
    vol = db['vols'].find_one({'NumVol': num_vol})
    
    if vol:
        ville_arrivee = vol.get("VilleA")
        
        if ville_arrivee:
            print(f"La ville d'arrivée pour le vol {num_vol} est : {ville_arrivee}")
        else:
            print(f"Aucune ville d'arrivée trouvée pour le vol {num_vol}.")
    else:
        print(f"Aucune donnée trouvée pour le vol {num_vol}.")

# Exemple d'exécution pour un vol donné
# Vous pouvez remplacer 'V117' par un autre numéro de vol existant dans votre base MongoDB
num_vol = "V909"  # Numéro de vol à rechercher
get_ville_arrivee(num_vol)

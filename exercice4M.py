# Trouver les vols entre deux villes données en utilisant MongoDB

from pymongo import MongoClient 

# Connexion à la base de données MongoDB
client = MongoClient('localhost', 27017)

# Sélection de la base de données
db = client['compagnie_aerienne']

def find_vols_between(ville_depart, ville_arrivee):
    # Rechercher les vols dans la collection 'vols' en utilisant 'VilleD' et 'VilleA' comme critères
    vols_cursor = db['vols'].find({'VilleD': ville_depart, 'VilleA': ville_arrivee})
    
    # Vérifier si des vols ont été trouvés
    vols_liste = list(vols_cursor)  # Convertir le curseur en liste pour pouvoir compter les éléments
    if len(vols_liste) > 0:
        print(f"Vols trouvés entre {ville_depart} et {ville_arrivee} :")
        for vol in vols_liste:
            # Extraire les informations pertinentes du vol
            num_vol = vol.get('NumVol')
            date_depart = vol.get('DateD')
            heure_depart = vol.get('HD time')
            # Afficher les informations du vol
            print(f"Numéro de vol : {num_vol}, Date de départ : {date_depart}, Heure de départ : {heure_depart}")
    else:
        # Si aucun vol n'a été trouvé
        print(f"Aucun vol trouvé entre {ville_depart} et {ville_arrivee}.")

# Exemple d'utilisation de la fonction
ville_depart = "Marseille" 
ville_arrivee = "Amsterdam" 
find_vols_between(ville_depart, ville_arrivee)

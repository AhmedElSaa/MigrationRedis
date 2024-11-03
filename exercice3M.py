# Séparer la base de données en deux et faire une jointure

import json   
from pymongo import MongoClient 

# Connexion à la base de données MongoDB
client = MongoClient('localhost', 27017)

# Sélection de la base de données
db = client['compagnie_aerienne']

# Accès à la collection 'vols' qui contient les vols
vols_collection = db['vols']

# Récupérer tous les vols depuis MongoDB
vols_cursor = vols_collection.find()

# Conversion du curseur en une liste de documents
vols_list = list(vols_cursor)

# Dictionnaire des vols avec 'NumVol' comme clé
vols = {vol['NumVol']: vol for vol in vols_list}

# Séparer les données en deux modèles
vols_keys = list(vols.keys()) 
mid_index = len(vols_keys) // 2 

# Modèle 1 : première moitié des vols
model_1_keys = vols_keys[:mid_index]  
model_1 = {key: vols[key] for key in model_1_keys}  

# Modèle 2 : seconde moitié des vols
model_2_keys = vols_keys[mid_index:]
model_2 = {key: vols[key] for key in model_2_keys} 


# Sauvegarder les modèles dans des fichiers JSON
with open('model_1M.json', 'w', encoding='utf-8') as f1:
    json.dump(model_1, f1, indent=4, default=str, ensure_ascii=False)

with open('model_2M.json', 'w', encoding='utf-8') as f2:
    json.dump(model_2, f2, indent=4, default=str, ensure_ascii=False) 

print("\nLes modèles ont été sauvegardés dans 'model_1M.json' et 'model_2M.json'.")

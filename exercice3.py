# Séparer la bdd en 2 et faire une jointure.
# Exemple en exemple.py

import json
import redis

# Connexion à la base de données Redis
r = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

# Récupérer tous les vols depuis Redis
vols = {}
for key in r.keys():
    # Vérifiez le type de la clé avant de tenter de la récupérer
    key_type = r.type(key)
    
    if key_type == 'string':
        value = r.get(key)
        try:
            vols[key] = json.loads(value)
        except json.JSONDecodeError:
            print(f"Erreur de décodage JSON pour la clé : {key}")
    else:
        print(f"Clé ignorée (type incorrect : {key_type}) : {key}")

# Séparer les données en deux modèles
keys = list(vols.keys())
mid_index = len(keys) // 2

# Modèle 1 : première moitié des vols
model_1 = {key: vols[key] for key in keys[:mid_index]}

# Modèle 2 : seconde moitié des vols
model_2 = {key: vols[key] for key in keys[mid_index:]}

# Affichage des résultats (ou éventuellement sauvegarde)
print("Modèle 1 (première moitié des vols) :")
print(json.dumps(model_1, indent=4))

print("\nModèle 2 (seconde moitié des vols) :")
print(json.dumps(model_2, indent=4))

# Sauvegarder les modèles dans des fichiers JSON
with open('model_1.json', 'w') as f1:
    json.dump(model_1, f1, indent=4)

with open('model_2.json', 'w') as f2:
    json.dump(model_2, f2, indent=4)

print("\nLes modèles ont été sauvegardés dans 'model_1.json' et 'model_2.json'.")
print(len(model_1)) # Nombre de données dans model 1
print(len(model_2)) # Nombre de données dans model 2

def jointure() : 
    return "z"
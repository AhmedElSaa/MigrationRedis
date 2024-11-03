# Séparer la base de données en deux et faire une jointure
# Exemple en exemple.py

import json   
import redis 

# Connexion à la base de données Redis
r = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

# Récupérer tous les vols depuis Redis
vols = {}
for key in r.keys():
    # Vérifier le type de la clé
    key_type = r.type(key)
    
    if key_type == 'string':
        # Si la clé est de type chaîne, nous pouvons récupérer sa valeur
        value = r.get(key)
        try:
            vols[key] = json.loads(value)
        except json.JSONDecodeError:
            print(f"Erreur de décodage JSON pour la clé : {key}")
    else:
        print(f"Clé ignorée (type incorrect : {key_type}) : {key}")

# Séparer les données en deux modèles
keys = list(vols.keys())          # Obtenir la liste des clés
mid_index = len(keys) // 2       

# Modèle 1 : première moitié des vols
model_1 = {key: vols[key] for key in keys[:mid_index]}

# Modèle 2 : seconde moitié des vols
model_2 = {key: vols[key] for key in keys[mid_index:]} 

# Sauvegarder les modèles dans des fichiers JSON
with open('model_1R.json', 'w') as f1:
    json.dump(model_1, f1, indent=4)  

with open('model_2R.json', 'w') as f2:
    json.dump(model_2, f2, indent=4)  

print("\nLes modèles ont été sauvegardés dans 'model_1R.json' et 'model_2R.json'.")


#Faire la jointure entre les 2 fichier, creer un dictionnaire et l'integrer dans la bdd

import json
import os
import redis

# Connexion à la base de données Redis
r = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

# Charger les deux fichiers JSON
with open('model_1.json', 'r') as f1:
    model_1 = json.load(f1)

with open('model_2.json', 'r') as f2:
    model_2 = json.load(f2)

def collecter_attribut(attribut):
    resultats = {}

    # Fonction pour parcourir un modèle et collecter les valeurs de l'attribut
    def collecter_valeurs(model):
        for vol_id, vol_data in model.items():
            # Rechercher dans la structure principale du vol
            if attribut in vol_data:
                resultats[vol_id] = vol_data[attribut]

            # Rechercher dans la section avion
            if 'avion' in vol_data and attribut in vol_data['avion']:
                resultats[vol_id] = vol_data['avion'][attribut]

            # Rechercher dans la section pilote
            if 'pilote' in vol_data and attribut in vol_data['pilote']:
                resultats[vol_id] = vol_data['pilote'][attribut]

            # Rechercher dans les réservations
            if 'reservations' in vol_data:
                for reservation_id, reservation_data in vol_data['reservations'].items():
                    if attribut in reservation_data:
                        resultats[vol_id] = reservation_data[attribut]
                    # Vérifier aussi dans les données du client
                    if 'client' in reservation_data and attribut in reservation_data['client']:
                        resultats[vol_id] = reservation_data['client'][attribut]

    # Collecter les valeurs de model_1 et model_2
    collecter_valeurs(model_1)
    collecter_valeurs(model_2)

    return resultats

# Appeler la fonction avec 'VilleD' comme attribut
attribut = ("VilleD")
resultats_dict = collecter_attribut(attribut)

# Afficher le dictionnaire résultant
#print(resultats_dict)

# Convertir le dictionnaire en format JSON pour le stocker dans Redis
resultat_formatte = json.dumps(resultats_dict)

# Stocker le résultat dans Redis
r.set(f"jointure_{attribut}", resultat_formatte)

# Vérification du stockage dans Redis
stocked_data = r.get(f"jointure_{attribut}")

# Afficher les données stockées
print("\nDonnées stockées dans Redis :")
print(stocked_data)





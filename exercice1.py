# Importer la base de données dans redis a partir de fichier a l'aide d'un programme python

import json
import os
import redis

# Connexion à la base de données Redis
r = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

# Table de correspondance des colonnes
tableCorespondance = {
    "AVIONS.txt": ["NumAv", "NomAv", "CapAv", "VilleAv"],
    "CLIENTS.txt": ["NumCl", "NomCl", "NumRuelCl", "NomRueCl", "CodePosteCl", "VileCl"],
    "DEFCLASSES.txt": ["NumVol", "Classe", "CoefPrix"],
    "PILOTES.txt": ["Numpil", "NomPil", "NaisPil", "VillePil"],
    "RESERVATIONS.txt": ["NumCl", "NumVol", "Classe", "NbPlaces"],
    "VOLS.txt": ["NumVol", "VilleD", "VilleA", "DateD", "HD time", "DateA", "HA time", "NumPil", "NumAv"],
}

# Lire les fichiers .txt et les stocker dans un dictionnaire JSON
dictAllJson = {}
for fileName in os.listdir("/iutv/Mes_Montages/12213849/tuto_redis_python/bddPilotes"):
    if fileName.endswith(".txt"):
        dictAllJson[fileName] = {}
        with open(os.path.join("/iutv/Mes_Montages/12213849/tuto_redis_python/bddPilotes", fileName), 'r') as fh:
            for line in fh:
                description = list(line.strip().split("\t"))
                dictAllJson[fileName][description[0]] = {}
                fields = tableCorespondance[fileName]
                for i, categorie in enumerate(fields[1:], start=1):
                    dictAllJson[fileName][description[0]][categorie] = description[i]

# Fusionner les informations dans un format imbriqué
jsonFinal = {}
idReserv = 0
for vol in dictAllJson["VOLS.txt"]:
    jsonFinal[vol] = dictAllJson["VOLS.txt"][vol]

    # Associer les avions
    for avion in dictAllJson["AVIONS.txt"]:
        if dictAllJson["VOLS.txt"][vol]["NumAv"] == avion:
            jsonFinal[vol]["avion"] = dictAllJson["AVIONS.txt"][avion]
    del(jsonFinal[vol]["NumAv"])

    # Associer les pilotes
    for pilote in dictAllJson["PILOTES.txt"]:
        if dictAllJson["VOLS.txt"][vol]["NumPil"] == pilote:
            jsonFinal[vol]["pilote"] = dictAllJson["PILOTES.txt"][pilote]
    del(jsonFinal[vol]["NumPil"])

    # Ajouter les réservations
    jsonFinal[vol]["reservations"] = {}
    for reserv in dictAllJson["RESERVATIONS.txt"]:
        if vol == dictAllJson["RESERVATIONS.txt"][reserv]["NumVol"]:
            jsonFinal[vol]["reservations"][str(idReserv)] = dictAllJson["RESERVATIONS.txt"][reserv]
            jsonFinal[vol]["reservations"][str(idReserv)]["NumCl"] = reserv

            # Associer les clients
            for client in dictAllJson["CLIENTS.txt"]:
                if jsonFinal[vol]["reservations"][str(idReserv)]["NumCl"] == client:
                    jsonFinal[vol]["reservations"][str(idReserv)]["client"] = dictAllJson["CLIENTS.txt"][client]
            del(jsonFinal[vol]["reservations"][str(idReserv)]["NumCl"])

            # Associer les classes
            for classe in dictAllJson["DEFCLASSES.txt"]:
                if dictAllJson["DEFCLASSES.txt"][classe]["Classe"] == jsonFinal[vol]["reservations"][str(idReserv)]["Classe"] and classe == vol:
                    jsonFinal[vol]["reservations"][str(idReserv)]["Classe"] = dictAllJson["DEFCLASSES.txt"][classe]
            idReserv += 1

# Insérer les données dans Redis
for vol_id, vol_data in jsonFinal.items():
    # Insérer chaque vol avec ses informations en tant que clé dans Redis
    r.set(vol_id, json.dumps(vol_data))
    print(vol_id,vol_data) # Voila tout ce qui s'insire dans la bdd 

print("Données insérées avec succès dans Redis.")

# Importer la base de données dans Redis à partir de fichiers texte à l'aide d'un programme Python

import json    
import os    
import redis   

# ... (autres fichiers)

# Connexion à la base de données Redis
r = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

# Table de correspondance des colonnes pour chaque fichier
tableCorrespondance = {
    "AVIONS.txt": ["NumAv", "NomAv", "CapAv", "VilleAv"],
    "CLIENTS.txt": ["NumCl", "NomCl", "NumRuelCl", "NomRueCl", "CodePosteCl", "VileCl"],
    "DEFCLASSES.txt": ["NumVol", "Classe", "CoefPrix"],
    "PILOTES.txt": ["Numpil", "NomPil", "NaisPil", "VillePil"],
    "RESERVATIONS.txt": ["NumCl", "NumVol", "Classe", "NbPlaces"],
    "VOLS.txt": ["NumVol", "VilleD", "VilleA", "DateD", "HD time", "DateA", "HA time", "NumPil", "NumAv"],
}

dictAllJson = {}

for fileName in os.listdir("C:/Users/elsaa/OneDrive/Bureau/BDD/bddPilotes"):
    if fileName.endswith(".txt"):
        dictAllJson[fileName] = {}
        # Ouvrir le fichier en mode lecture
        with open(os.path.join("C:/Users/elsaa/OneDrive/Bureau/BDD/bddPilotes", fileName), 'r') as fh:
            # Lire chaque ligne du fichier
            for line in fh:
                # Supprimer les espaces en début et fin de ligne, puis diviser la ligne en utilisant la tabulation comme séparateur
                description = list(line.strip().split("\t"))
                
                # Récupérer la liste des noms de colonnes pour ce fichier
                fields = tableCorrespondance[fileName]
                # Vérifier que le nombre de valeurs correspond au nombre de colonnes attendues
                if len(description) < len(fields):
                    print(f"Ligne ignorée dans {fileName} : {line.strip()} - Nombre de colonnes insuffisant.")
                    continue

                # Stocker les données dans le dictionnaire
                dictAllJson[fileName][description[0]] = {}
                # Parcourir les colonnes restantes et associer chaque valeur à son nom de colonne
                for i, categorie in enumerate(fields[1:], start=1):
                    dictAllJson[fileName][description[0]][categorie] = description[i]

# Fusionner les informations dans un format imbriqué pour faciliter l'insertion dans Redis
jsonFinal = {}
idReserv = 0    

# Parcourir chaque vol dans les données de VOLS.txt
for vol in dictAllJson["VOLS.txt"]:
    jsonFinal[vol] = dictAllJson["VOLS.txt"][vol]
    
    # Associer les informations de l'avion au vol
    for avion in dictAllJson["AVIONS.txt"]:
        if dictAllJson["VOLS.txt"][vol]["NumAv"] == avion:
            # Ajouter les informations de l'avion au vol
            jsonFinal[vol]["avion"] = dictAllJson["AVIONS.txt"][avion]
    # Supprimer la clé 'NumAv' car les informations de l'avion sont maintenant incluses
    del(jsonFinal[vol]["NumAv"])

    # Associer les informations du pilote au vol
    for pilote in dictAllJson["PILOTES.txt"]:
        # Vérifier si le numéro du pilote correspond
        if dictAllJson["VOLS.txt"][vol]["NumPil"] == pilote:
            # Ajouter les informations du pilote au vol
            jsonFinal[vol]["pilote"] = dictAllJson["PILOTES.txt"][pilote]
    # Supprimer la clé 'NumPil' car les informations du pilote sont maintenant incluses
    del(jsonFinal[vol]["NumPil"])

    # Initialiser un dictionnaire pour les réservations associées à ce vol
    jsonFinal[vol]["reservations"] = {}
    # Parcourir toutes les réservations
    for reserv in dictAllJson["RESERVATIONS.txt"]:
        # Vérifier si la réservation concerne ce vol
        if vol == dictAllJson["RESERVATIONS.txt"][reserv]["NumVol"]:
            # Ajouter la réservation au dictionnaire des réservations du vol
            jsonFinal[vol]["reservations"][str(idReserv)] = dictAllJson["RESERVATIONS.txt"][reserv]
            # Ajouter le numéro du client à la réservation
            jsonFinal[vol]["reservations"][str(idReserv)]["NumCl"] = reserv

            # Associer les informations du client à la réservation
            for client in dictAllJson["CLIENTS.txt"]:
                # Vérifier si le numéro du client correspond
                if jsonFinal[vol]["reservations"][str(idReserv)]["NumCl"] == client:
                    # Ajouter les informations du client à la réservation
                    jsonFinal[vol]["reservations"][str(idReserv)]["client"] = dictAllJson["CLIENTS.txt"][client]
            # Supprimer la clé 'NumCl' car les informations du client sont maintenant incluses
            del(jsonFinal[vol]["reservations"][str(idReserv)]["NumCl"])

            # Associer les informations de la classe à la réservation
            for classe in dictAllJson["DEFCLASSES.txt"]:
                # Vérifier si la classe correspond et si elle est associée à ce vol
                if (dictAllJson["DEFCLASSES.txt"][classe]["Classe"] == jsonFinal[vol]["reservations"][str(idReserv)]["Classe"]
                    and classe == vol):
                    # Remplacer la valeur 'Classe' par les informations détaillées de la classe
                    jsonFinal[vol]["reservations"][str(idReserv)]["Classe"] = dictAllJson["DEFCLASSES.txt"][classe]
            # Incrémenter l'identifiant de réservation pour la prochaine réservation
            idReserv += 1

# Parcourir chaque pilote dans les données de PILOTES.txt
for pilote_id, pilote_data in dictAllJson["PILOTES.txt"].items():
    # Créer une clé unique pour chaque pilote, par exemple 'PILOTE:<NumPil>'
    pilote_key = f"PILOTE:{pilote_id}"
    # Convertir les données du pilote en chaîne JSON
    pilote_json = json.dumps(pilote_data)
    # Insérer le pilote dans Redis avec sa clé unique
    r.set(pilote_key, pilote_json)

# Insérer les données des vols (avec les pilotes imbriqués) dans Redis
for vol_id, vol_data in jsonFinal.items():
    # Convertir les données du vol en chaîne JSON
    vol_json = json.dumps(vol_data)
    # Insérer chaque vol dans Redis avec son identifiant comme clé
    r.set(vol_id, vol_json)

# Afficher un message une fois que toutes les données ont été insérées
print("Données insérées avec succès dans Redis.")
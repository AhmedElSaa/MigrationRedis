import os
from pymongo import MongoClient

# Connexion à la base de données MongoDB
client = MongoClient('localhost', 27017)
db = client['compagnie_aerienne']  

# Table de correspondance des colonnes pour chaque fichier
tableCorrespondance = {
    "AVIONS.txt": ["NumAv", "NomAv", "CapAv", "VilleAv"],
    "CLIENTS.txt": ["NumCl", "NomCl", "NumRuelCl", "NomRueCl", "CodePosteCl", "VileCl"],
    "DEFCLASSES.txt": ["NumVol", "Classe", "CoefPrix"],
    "PILOTES.txt": ["Numpil", "NomPil", "NaisPil", "VillePil"],
    "RESERVATIONS.txt": ["NumCl", "NumVol", "Classe", "NbPlaces"],
    "VOLS.txt": ["NumVol", "VilleD", "VilleA", "DateD", "HD time", "DateA", "HA time", "NumPil", "NumAv"],
}


# Parcourir tous les fichiers du répertoire spécifié
for fileName in os.listdir("C:/Users/elsaa/OneDrive/Bureau/BDD/bddPilotes"):
    if fileName.endswith(".txt"):
        with open(os.path.join("C:/Users/elsaa/OneDrive/Bureau/BDD/bddPilotes", fileName), 'r') as fh:
            # Préparer une liste pour stocker les documents à insérer
            documents = []
            # Lire chaque ligne du fichier
            for line in fh:
                # Supprimer les espaces en début et fin de ligne, puis diviser la ligne en utilisant la tabulation comme séparateur
                description = list(line.strip().split("\t"))
                
                # Récupérer la liste des noms de colonnes pour ce fichier
                fields = tableCorrespondance[fileName]
                # Vérifier que le nombre de valeurs correspond au nombre de colonnes attendues
                if len(description) < len(fields):
                    print(f"Ligne ignorée dans {fileName} : {line.strip()} - Nombre de colonnes insuffisant.")
                    continue  # Ignorer cette ligne et passer à la suivante

                # Créer un dictionnaire pour le document
                document = {}
                for i, field in enumerate(fields):
                    document[field] = description[i]
                documents.append(document)
            # Insérer les documents dans une collection MongoDB
            collection_name = fileName.replace('.txt', '').lower()  # Nom de la collection (par exemple, 'avions')
            db[collection_name].insert_many(documents)
            print(f"{len(documents)} documents insérés dans la collection '{collection_name}'.")

#show dbs
#use compagnie_aerienne
#db.vols.countDocuments()
#db.vols.find()
#db.dropDatabase()

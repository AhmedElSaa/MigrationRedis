# Trouver le nombre total de pilotes dans la base de données MongoDB

from pymongo import MongoClient 

client = MongoClient('localhost', 27017)

# Sélection de la base de données
db = client['compagnie_aerienne']

def count_pilots():

    # Sélectionner la collection 'pilotes'
    pilotes_collection = db['pilotes']
    
    # Compter le nombre total de documents dans la collection 'pilotes'
    nombre_pilotes = pilotes_collection.count_documents({})
    
    # Afficher le nombre de pilotes trouvés
    print(f"Nombre de pilotes trouvés dans MongoDB : {nombre_pilotes}")

count_pilots()

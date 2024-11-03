# Trouver le nombre total de pilotes dans la base de données Redis

import redis

r = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

def count_pilots():
    # Récupérer toutes les clés des pilotes
    pilote_keys = r.keys("PILOTE:*")
    
    # Afficher le nombre de pilotes trouvés
    print(f"Nombre de pilotes trouvés dans Redis : {len(pilote_keys)}")

count_pilots()

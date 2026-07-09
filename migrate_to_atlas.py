"""
Utilise ce script pour copier tes données locales vers MongoDB Atlas.

1. Crée un cluster gratuit sur https://www.mongodb.com/atlas
2. Clique sur "Connect" → "Drivers" → copie l'URI
3. Lance :
   python3 migrate_to_atlas.py "ton_uri_atlas"
"""

import sys
from pymongo import MongoClient

LOCAL_URI = "mongodb://localhost:27017"
ATLAS_URI = sys.argv[1] if len(sys.argv) > 1 else None

if not ATLAS_URI:
    print("Usage: python3 migrate_to_atlas.py \"mongodb+srv://user:pass@cluster.xxxxx.mongodb.net/\"")
    sys.exit(1)

local = MongoClient(LOCAL_URI)
atlas = MongoClient(ATLAS_URI)

local_col = local["gestion_etudiants"]["students"]
atlas_col = atlas["gestion_etudiants"]["students"]

data = list(local_col.find({}))
if not data:
    print("Aucune donnée à migrer.")
    sys.exit(0)

# Supprime _id pour éviter les doublons
for d in data:
    d.pop("_id", None)

atlas_col.delete_many({})
atlas_col.insert_many(data)
print(f"{len(data)} étudiant(s) migré(s) vers MongoDB Atlas !")

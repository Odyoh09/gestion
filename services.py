from database import students_collection
from models import Student
from bson import ObjectId


def ajouter_etudiant(student):
    if students_collection.find_one({"numero_etudiant": student.numero_etudiant}):
        print(f"Erreur : Le numéro étudiant {student.numero_etudiant} existe déjà.")
        return False
    result = students_collection.insert_one(student.to_dict())
    print(f"Étudiant ajouté avec l'ID : {result.inserted_id}")
    return True


def lister_etudiants():
    etudiants = students_collection.find()
    return list(etudiants)


def rechercher_etudiant(cle, valeur):
    query = {cle: {"$regex": valeur, "$options": "i"}}
    return list(students_collection.find(query))


def mettre_a_jour_etudiant(numero_etudiant, updates):
    result = students_collection.update_one(
        {"numero_etudiant": numero_etudiant},
        {"$set": updates}
    )
    if result.matched_count == 0:
        print(f"Aucun étudiant trouvé avec le numéro {numero_etudiant}.")
        return False
    print(f"{result.modified_count} champ(s) mis à jour.")
    return True


def supprimer_etudiant(numero_etudiant):
    result = students_collection.delete_one({"numero_etudiant": numero_etudiant})
    if result.deleted_count == 0:
        print(f"Aucun étudiant trouvé avec le numéro {numero_etudiant}.")
        return False
    print(f"Étudiant {numero_etudiant} supprimé.")
    return True


def get_statistiques():
    total = students_collection.count_documents({})
    filieres = students_collection.distinct("filiere")
    stats_filieres = {}
    for f in filieres:
        count = students_collection.count_documents({"filiere": f})
        stats_filieres[f] = count
    return {"total": total, "par_filiere": stats_filieres}

from database import students_collection
from models import Student
import random

classes = ["L1", "L2", "L3", "M1", "M2"]
sample_students = [
    ("Dupont", "Jean", 22, "jean.dupont@email.com", "Informatique", "L3", "ETU001"),
    ("Martin", "Sophie", 21, "sophie.martin@email.com", "Mathématiques", "L2", "ETU002"),
    ("Diallo", "Amadou", 23, "amadou.diallo@email.com", "Physique", "M1", "ETU003"),
    ("Koné", "Fatou", 20, "fatou.kone@email.com", "Informatique", "L1", "ETU004"),
    ("Traoré", "Moussa", 24, "moussa.traore@email.com", "Chimie", "M2", "ETU005"),
    ("Ndiaye", "Aïcha", 22, "aicha.ndiaye@email.com", "Mathématiques", "L3", "ETU006"),
    ("Kouassi", "Paul", 21, "paul.kouassi@email.com", "Informatique", "L2", "ETU007"),
    ("Bamba", "Mariam", 23, "mariam.bamba@email.com", "Physique", "M1", "ETU008"),
    ("Touré", "Oumar", 25, "oumar.toure@email.com", "Électronique", "M2", "ETU009"),
    ("Camara", "Aminata", 20, "aminata.camara@email.com", "Informatique", "L1", "ETU010"),
]

for nom, prenom, age, email, filiere, classe, numero in sample_students:
    if not students_collection.find_one({"numero_etudiant": numero}):
        student = Student(nom, prenom, age, email, filiere, numero)
        data = student.to_dict()
        data["classe"] = classe
        data["moyenne"] = round(random.uniform(8, 18), 2)
        students_collection.insert_one(data)
        print(f"  + {numero} - {nom} {prenom} ({classe})")
    else:
        print(f"  ~ {numero} déjà existant")

print(f"\nTotal: {students_collection.count_documents({})} étudiants")

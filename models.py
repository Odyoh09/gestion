from datetime import datetime


class Student:
    def __init__(self, nom, prenom, age, email, filiere, numero_etudiant):
        self.nom = nom
        self.prenom = prenom
        self.age = age
        self.email = email
        self.filiere = filiere
        self.numero_etudiant = numero_etudiant
        self.date_inscription = datetime.now().isoformat()

    def to_dict(self):
        return {
            "nom": self.nom,
            "prenom": self.prenom,
            "age": self.age,
            "email": self.email,
            "filiere": self.filiere,
            "numero_etudiant": self.numero_etudiant,
            "date_inscription": self.date_inscription,
        }

    @staticmethod
    def from_dict(data):
        return Student(
            nom=data["nom"],
            prenom=data["prenom"],
            age=data["age"],
            email=data["email"],
            filiere=data["filiere"],
            numero_etudiant=data["numero_etudiant"],
        )

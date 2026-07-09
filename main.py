from models import Student
from services import (
    ajouter_etudiant,
    lister_etudiants,
    rechercher_etudiant,
    mettre_a_jour_etudiant,
    supprimer_etudiant,
    get_statistiques,
)


def afficher_menu():
    print("\n" + "=" * 45)
    print("   GESTION DES ÉTUDIANTS - MENU PRINCIPAL")
    print("=" * 45)
    print("1.  Ajouter un étudiant")
    print("2.  Lister tous les étudiants")
    print("3.  Rechercher un étudiant")
    print("4.  Mettre à jour un étudiant")
    print("5.  Supprimer un étudiant")
    print("6.  Voir les statistiques")
    print("0.  Quitter")
    print("=" * 45)


def afficher_etudiant(e):
    print(f"  ID MongoDB      : {e['_id']}")
    print(f"  Numéro étudiant : {e['numero_etudiant']}")
    print(f"  Nom             : {e['nom']}")
    print(f"  Prénom          : {e['prenom']}")
    print(f"  Âge             : {e['age']}")
    print(f"  Email           : {e['email']}")
    print(f"  Filière         : {e['filiere']}")
    print(f"  Date inscription: {e['date_inscription']}")
    print("-" * 45)


def saisir_etudiant():
    nom = input("Nom : ").strip()
    prenom = input("Prénom : ").strip()
    age = int(input("Âge : ").strip())
    email = input("Email : ").strip()
    filiere = input("Filière : ").strip()
    numero = input("Numéro étudiant : ").strip()
    return Student(nom, prenom, age, email, filiere, numero)


def menu_ajouter():
    print("\n--- Ajouter un étudiant ---")
    student = saisir_etudiant()
    ajouter_etudiant(student)


def menu_lister():
    print("\n--- Liste des étudiants ---")
    etudiants = lister_etudiants()
    if not etudiants:
        print("Aucun étudiant trouvé.")
        return
    print(f"Total : {len(etudiants)} étudiant(s)\n")
    for e in etudiants:
        afficher_etudiant(e)


def menu_rechercher():
    print("\n--- Rechercher un étudiant ---")
    print("Champs : nom, prenom, email, filiere, numero_etudiant")
    cle = input("Champ à rechercher : ").strip()
    valeur = input("Valeur : ").strip()
    resultats = rechercher_etudiant(cle, valeur)
    if not resultats:
        print("Aucun résultat.")
        return
    print(f"\n{len(resultats)} résultat(s) :\n")
    for e in resultats:
        afficher_etudiant(e)


def menu_modifier():
    print("\n--- Modifier un étudiant ---")
    numero = input("Numéro étudiant à modifier : ").strip()
    print("Laissez vide pour ne pas modifier un champ.")
    updates = {}
    for champ in ["nom", "prenom", "email", "filiere"]:
        val = input(f"Nouveau {champ} : ").strip()
        if val:
            updates[champ] = val
    age = input("Nouvel âge : ").strip()
    if age:
        updates["age"] = int(age)
    if updates:
        mettre_a_jour_etudiant(numero, updates)
    else:
        print("Aucune modification demandée.")


def menu_supprimer():
    print("\n--- Supprimer un étudiant ---")
    numero = input("Numéro étudiant à supprimer : ").strip()
    supprimer_etudiant(numero)


def menu_statistiques():
    stats = get_statistiques()
    print("\n--- Statistiques ---")
    print(f"Total étudiants : {stats['total']}")
    print("Par filière :")
    for filiere, count in stats["par_filiere"].items():
        print(f"  - {filiere} : {count}")


def main():
    while True:
        afficher_menu()
        choix = input("Votre choix : ").strip()
        if choix == "1":
            menu_ajouter()
        elif choix == "2":
            menu_lister()
        elif choix == "3":
            menu_rechercher()
        elif choix == "4":
            menu_modifier()
        elif choix == "5":
            menu_supprimer()
        elif choix == "6":
            menu_statistiques()
        elif choix == "0":
            print("Au revoir !")
            break
        else:
            print("Choix invalide. Veuillez réessayer.")


if __name__ == "__main__":
    main()

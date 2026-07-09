from flask import Flask, render_template, request, redirect, url_for, flash
from database import db, students_collection
from models import Student

app = Flask(__name__)
app.secret_key = "gestion-etudiants-secret-key-2024"


@app.route("/")
def dashboard():
    total = students_collection.count_documents({})
    filieres = students_collection.distinct("filiere")
    stats_filieres = {}
    for f in filieres:
        count = students_collection.count_documents({"filiere": f})
        stats_filieres[f] = count
    max_count = max(stats_filieres.values()) if stats_filieres else 1
    return render_template("dashboard.html", total=total, stats=stats_filieres, max_count=max_count)


@app.route("/etudiants")
def lister():
    etudiants = students_collection.find().sort("date_inscription", -1)
    return render_template("lister.html", etudiants=list(etudiants))


@app.route("/ajouter", methods=["GET", "POST"])
def ajouter():
    if request.method == "POST":
        data = request.form
        exists = students_collection.find_one({"numero_etudiant": data["numero_etudiant"]})
        if exists:
            flash("Ce numéro étudiant existe déjà.", "danger")
            return render_template("ajouter.html")
        student = Student(
            nom=data["nom"],
            prenom=data["prenom"],
            age=int(data["age"]),
            email=data["email"],
            filiere=data["filiere"],
            numero_etudiant=data["numero_etudiant"],
        )
        students_collection.insert_one(student.to_dict())
        flash("Étudiant ajouté avec succès.", "success")
        return redirect(url_for("lister"))
    return render_template("ajouter.html")


@app.route("/modifier/<numero_etudiant>", methods=["GET", "POST"])
def modifier(numero_etudiant):
    etudiant = students_collection.find_one({"numero_etudiant": numero_etudiant})
    if not etudiant:
        flash("Étudiant introuvable.", "danger")
        return redirect(url_for("lister"))

    if request.method == "POST":
        updates = {}
        for champ in ["nom", "prenom", "email", "filiere"]:
            val = request.form.get(champ, "").strip()
            if val:
                updates[champ] = val
        age = request.form.get("age", "").strip()
        if age:
            updates["age"] = int(age)
        if updates:
            students_collection.update_one({"numero_etudiant": numero_etudiant}, {"$set": updates})
            flash("Étudiant modifié avec succès.", "success")
            return redirect(url_for("lister"))
    return render_template("modifier.html", etudiant=etudiant)


@app.route("/supprimer/<numero_etudiant>")
def supprimer(numero_etudiant):
    result = students_collection.delete_one({"numero_etudiant": numero_etudiant})
    if result.deleted_count:
        flash("Étudiant supprimé avec succès.", "success")
    else:
        flash("Étudiant introuvable.", "danger")
    return redirect(url_for("lister"))


@app.route("/rechercher")
def rechercher():
    q = request.args.get("q", "").strip()
    champ = request.args.get("champ", "nom")
    resultats = []
    if q:
        query = {champ: {"$regex": q, "$options": "i"}}
        resultats = list(students_collection.find(query))
    return render_template("rechercher.html", resultats=resultats, q=q, champ=champ)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8501, debug=True)

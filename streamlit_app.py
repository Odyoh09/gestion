import streamlit as st
from pymongo import MongoClient
from datetime import datetime
import os

MONGO_URI = st.secrets.get("MONGO_URI") or os.getenv("MONGO_URI") or "mongodb://localhost:27017"
client = MongoClient(MONGO_URI)
db = client["gestion_etudiants"]
col = db["students"]

st.set_page_config(page_title="Gestion Étudiants", page_icon="🎓", layout="wide")

st.markdown("""
<style>
.stApp { background: #0f0f0f; }
.stTabs [data-baseweb="tab-list"] { gap: 2px; }
.stTabs [data-baseweb="tab"] { border-radius: 8px 8px 0 0 !important; font-weight: 600; }
[data-testid="stMetricValue"] { font-size: 28px !important; font-weight: 700 !important; }
.stButton button { border-radius: 8px; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

st.title("🎓 Gestion des Étudiants")

CLASSES = ["L1", "L2", "L3", "M1", "M2", "Doctorat"]

tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "📋 Liste", "➕ Ajouter", "🔍 Rechercher"])

with tab1:
    total = col.count_documents({})
    filieres = col.distinct("filiere")
    classes = col.distinct("classe")
    stats_fil = {f: col.count_documents({"filiere": f}) for f in filieres}
    stats_cls = {c: col.count_documents({"classe": c}) for c in classes}

    ages = list(col.find({}, {"age": 1, "_id": 0}))
    moyenne_age = round(sum(a["age"] for a in ages) / len(ages), 1) if ages else 0

    moyennes = list(col.find({}, {"moyenne": 1, "_id": 0}))
    moyenne_gen = round(sum(m["moyenne"] for m in moyennes) / len(moyennes), 2) if moyennes else 0

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total", total)
    c2.metric("Âge moyen", moyenne_age)
    c3.metric("Moy. générale", moyenne_gen)
    c4.metric("Filières", len(filieres))
    c5.metric("Classes", len(classes))

    if stats_cls:
        st.subheader("Moyenne par classe")
        for cls in CLASSES:
            if cls in stats_cls:
                moy_cls = list(col.find({"classe": cls}, {"moyenne": 1, "_id": 0}))
                moy = round(sum(m["moyenne"] for m in moy_cls) / len(moy_cls), 2) if moy_cls else 0
                st.markdown(f"**{cls}** ({stats_cls[cls]} ét.) — {moy}/20")
                st.progress(int(moy / 20 * 100))

    if stats_fil:
        st.subheader("Répartition par filière")
        for f, count in stats_fil.items():
            st.markdown(f"**{f}** ({count})")
            st.progress(int(count / max(stats_fil.values()) * 100))
    else:
        st.info("Aucun étudiant inscrit.")

with tab2:
    etudiants = list(col.find().sort("date_inscription", -1))
    if etudiants:
        for e in etudiants:
            with st.container(border=True):
                cols = st.columns([1, 2, 1, 1, 1, 1, 1, 1])
                cols[0].markdown(f"**{e['numero_etudiant']}**")
                cols[1].write(f"{e['nom']} {e['prenom']}")
                cols[2].write(e.get("classe", ""))
                cols[3].write(e["age"])
                cols[4].write(e.get("moyenne", ""))
                cols[5].markdown(f"`{e['filiere']}`")
                if cols[6].button("✏️", key=f"edit_{e['numero_etudiant']}"):
                    st.session_state.edit_num = e["numero_etudiant"]
                    st.rerun()
                if cols[7].button("🗑", key=f"del_{e['numero_etudiant']}"):
                    col.delete_one({"numero_etudiant": e["numero_etudiant"]})
                    st.rerun()

    if "edit_num" in st.session_state and st.session_state.edit_num:
        e = col.find_one({"numero_etudiant": st.session_state.edit_num})
        if e:
            st.markdown("---")
            st.subheader(f"Modifier {e['nom']} {e['prenom']}")
            with st.form("edit_form"):
                c1, c2 = st.columns(2)
                with c1:
                    nom = st.text_input("Nom", value=e["nom"])
                    prenom = st.text_input("Prénom", value=e["prenom"])
                    age = st.number_input("Âge", 16, 99, e["age"])
                    classe = st.selectbox("Classe", CLASSES, index=CLASSES.index(e.get("classe", "L1")))
                with c2:
                    email = st.text_input("Email", value=e["email"])
                    filiere = st.text_input("Filière", value=e["filiere"])
                    moyenne = st.number_input("Moyenne", 0.0, 20.0, float(e.get("moyenne", 0)), step=0.5)
                col1, col2 = st.columns(2)
                with col1:
                    if st.form_submit_button("Enregistrer", type="primary", use_container_width=True):
                        col.update_one(
                            {"numero_etudiant": e["numero_etudiant"]},
                            {"$set": {"nom": nom, "prenom": prenom, "age": age, "email": email, "filiere": filiere, "classe": classe, "moyenne": moyenne}}
                        )
                        st.success("Modifié !")
                        st.session_state.edit_num = None
                        st.rerun()
                with col2:
                    if st.form_submit_button("Annuler", use_container_width=True):
                        st.session_state.edit_num = None
                        st.rerun()
    else:
        st.info("Aucun étudiant.")

with tab3:
    with st.form("add_form"):
        c1, c2 = st.columns(2)
        with c1:
            nom = st.text_input("Nom")
            prenom = st.text_input("Prénom")
            age = st.number_input("Âge", 16, 99, 20)
            classe = st.selectbox("Classe", CLASSES)
        with c2:
            email = st.text_input("Email")
            filiere = st.text_input("Filière")
            numero = st.text_input("N° Étudiant")
            moyenne = st.number_input("Moyenne", 0.0, 20.0, 0.0, step=0.5)

        if st.form_submit_button("Ajouter", type="primary", use_container_width=True):
            if nom and prenom and email and filiere and numero and classe:
                if col.find_one({"numero_etudiant": numero}):
                    st.error("Ce numéro existe déjà.")
                else:
                    col.insert_one({
                        "nom": nom, "prenom": prenom, "age": age,
                        "email": email, "filiere": filiere, "classe": classe,
                        "moyenne": moyenne,
                        "numero_etudiant": numero,
                        "date_inscription": datetime.now().isoformat()
                    })
                    st.success("Étudiant ajouté !")
                    st.rerun()
            else:
                st.error("Tous les champs sont requis.")

with tab4:
    champ = st.selectbox("Chercher par", ["nom", "prenom", "email", "filiere", "classe", "numero_etudiant"])
    q = st.text_input("Recherche")
    if q:
        resultats = list(col.find({champ: {"$regex": q, "$options": "i"}}))
        if resultats:
            st.write(f"{len(resultats)} résultat(s)")
            for e in resultats:
                with st.container(border=True):
                    st.markdown(f"**{e['numero_etudiant']}** — {e['nom']} {e['prenom']} — {e.get('classe','')} — `{e['filiere']}` — **{e.get('moyenne',0)}/20**")
        else:
            st.info("Aucun résultat.")

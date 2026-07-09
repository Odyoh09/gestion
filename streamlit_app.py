import streamlit as st
from pymongo import MongoClient
from datetime import datetime
import os

st.set_page_config(page_title="Gestion Etudiants", page_icon=":material/school:", layout="wide")

st.markdown("""
<style>
.stApp { background: #0f0f0f; }
.stTabs [data-baseweb="tab-list"] { gap: 2px; }
.stTabs [data-baseweb="tab"] { border-radius: 8px 8px 0 0 !important; font-weight: 600; }
[data-testid="stMetricValue"] { font-size: 28px !important; font-weight: 700 !important; }
.stButton button { border-radius: 8px; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

st.title("Gestion des Etudiants")

@st.cache_resource
def init_conn():
    MONGO_URI = st.secrets.get("MONGO_URI") or os.getenv("MONGO_URI") or "mongodb://localhost:27017"
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        client.admin.command("ping")
        return client["gestion_etudiants"]["students"]
    except Exception:
        return None

col = init_conn()

if col is None:
    st.error("Connexion MongoDB impossible.\n\n"
             "Verifie que :\n"
             "1. L'URI dans Streamlit Cloud (Settings > Secrets) est correct\n"
             "2. MongoDB Atlas > Network Access > 0.0.0.0/0 est autorise\n"
             "3. Database Access > l'utilisateur a les droits sur la base")
    st.stop()

CLASSES = ["L1", "L2", "L3", "M1", "M2", "Doctorat"]

tab1, tab2, tab3, tab4 = st.tabs(["Dashboard", "Liste", "Ajouter", "Rechercher"])

with tab1:
    total = col.count_documents({})
    stats_fil = {}
    stats_cls = {}
    for f in col.distinct("filiere"):
        stats_fil[f] = col.count_documents({"filiere": f})
    for c in col.distinct("classe"):
        stats_cls[c] = col.count_documents({"classe": c})

    ages = [a["age"] for a in col.find({}, {"age": 1, "_id": 0})]
    moyenne_age = round(sum(ages) / len(ages), 1) if ages else 0

    moyennes = [m["moyenne"] for m in col.find({}, {"moyenne": 1, "_id": 0})]
    moyenne_gen = round(sum(moyennes) / len(moyennes), 2) if moyennes else 0

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total", total)
    c2.metric("Age moyen", moyenne_age)
    c3.metric("Moy. generale", moyenne_gen)
    c4.metric("Filieres", len(stats_fil))
    c5.metric("Classes", len(stats_cls))

    if stats_cls:
        st.subheader("Moyenne par classe")
        for cls in CLASSES:
            if cls in stats_cls:
                m = [x["moyenne"] for x in col.find({"classe": cls}, {"moyenne": 1, "_id": 0})]
                moy = round(sum(m) / len(m), 2) if m else 0
                st.markdown(f"**{cls}** ({stats_cls[cls]} et.)  {moy}/20")
                st.progress(int(moy / 20 * 100))

    if stats_fil:
        st.subheader("Repartition par filiere")
        mx = max(stats_fil.values())
        for f, c in stats_fil.items():
            st.markdown(f"**{f}** ({c})")
            st.progress(int(c / mx * 100))
    else:
        st.info("Aucun etudiant inscrit.")

with tab2:
    etudiants = list(col.find().sort("date_inscription", -1))
    if etudiants:
        for e in etudiants:
            with st.container(border=True):
                cols = st.columns([1, 2, 1, 1, 1, 1, 1, 1])
                cols[0].markdown(f"**{e['numero_etudiant']}**")
                cols[1].write(f"{e['nom']} {e['prenom']}")
                cols[2].write(e.get("classe", ""))
                cols[3].write(str(e["age"]))
                cols[4].write(str(e.get("moyenne", "")))
                cols[5].markdown(f"`{e['filiere']}`")
                if cols[6].button("Modifier", key=f"e_{e['numero_etudiant']}"):
                    st.session_state.edit_num = e["numero_etudiant"]
                    st.rerun()
                if cols[7].button("Suppr", key=f"d_{e['numero_etudiant']}"):
                    col.delete_one({"numero_etudiant": e["numero_etudiant"]})
                    st.rerun()

        if "edit_num" in st.session_state and st.session_state.edit_num:
            e = col.find_one({"numero_etudiant": st.session_state.edit_num})
            if e:
                st.markdown("---")
                st.subheader(f"Modifier {e['nom']} {e['prenom']}")
                with st.form("edit_form"):
                    col1, col2 = st.columns(2)
                    with col1:
                        nom = st.text_input("Nom", value=e["nom"])
                        prenom = st.text_input("Prenom", value=e["prenom"])
                        age = st.number_input("Age", 16, 99, e["age"])
                        classe = st.selectbox("Classe", CLASSES, index=CLASSES.index(e.get("classe", "L1")))
                    with col2:
                        email = st.text_input("Email", value=e["email"])
                        filiere = st.text_input("Filiere", value=e["filiere"])
                        moyenne = st.number_input("Moyenne", 0.0, 20.0, float(e.get("moyenne", 0)), step=0.5)
                    b1, b2 = st.columns(2)
                    with b1:
                        if st.form_submit_button("Enregistrer", type="primary", use_container_width=True):
                            col.update_one({"numero_etudiant": e["numero_etudiant"]},
                                {"$set": {"nom": nom, "prenom": prenom, "age": age, "email": email,
                                          "filiere": filiere, "classe": classe, "moyenne": moyenne}})
                            st.session_state.edit_num = None
                            st.rerun()
                    with b2:
                        if st.form_submit_button("Annuler", use_container_width=True):
                            st.session_state.edit_num = None
                            st.rerun()
    else:
        st.info("Aucun etudiant.")

with tab3:
    with st.form("add_form"):
        c1, c2 = st.columns(2)
        with c1:
            nom = st.text_input("Nom")
            prenom = st.text_input("Prenom")
            age = st.number_input("Age", 16, 99, 20)
            classe = st.selectbox("Classe", CLASSES)
        with c2:
            email = st.text_input("Email")
            filiere = st.text_input("Filiere")
            numero = st.text_input("No Etudiant")
            moyenne = st.number_input("Moyenne", 0.0, 20.0, 0.0, step=0.5)

        if st.form_submit_button("Ajouter", type="primary", use_container_width=True):
            if not all([nom, prenom, email, filiere, numero, classe]):
                st.error("Tous les champs sont requis.")
            elif col.find_one({"numero_etudiant": numero}):
                st.error("Ce numero existe deja.")
            else:
                col.insert_one({"nom": nom, "prenom": prenom, "age": age, "email": email,
                                "filiere": filiere, "classe": classe, "moyenne": moyenne,
                                "numero_etudiant": numero,
                                "date_inscription": datetime.now().isoformat()})
                st.success("Etudiant ajoute !")
                st.rerun()

with tab4:
    col1, col2 = st.columns([1, 2])
    with col1:
        champ = st.selectbox("Chercher par", ["nom", "prenom", "email", "filiere", "classe", "numero_etudiant"])
    with col2:
        q = st.text_input("Recherche", label_visibility="collapsed", placeholder="Rechercher...")
    if q:
        resultats = list(col.find({champ: {"$regex": q, "$options": "i"}}))
        if resultats:
            st.write(f"{len(resultats)} resultat(s)")
            for e in resultats:
                with st.container(border=True):
                    st.markdown(f"**{e['numero_etudiant']}** - {e['nom']} {e['prenom']} - {e.get('classe','')} - `{e['filiere']}` - **{e.get('moyenne',0)}/20**")
        else:
            st.info("Aucun resultat.")

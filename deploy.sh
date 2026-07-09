#!/bin/bash
# Script pour déployer sur Streamlit Cloud
# Prérequis : avoir un dépôt GitHub et un cluster MongoDB Atlas

echo "=== Déploiement Gestion Étudiants ==="
echo ""
echo "1. Crée un cluster gratuit sur https://www.mongodb.com/atlas"
echo "2. Va dans Security → Database Access → Add New User"
echo "3. Va dans Network Access → Add IP → 0.0.0.0/0"
echo "4. Clique sur Connect → Drivers → copie l'URI"
echo ""
echo "5. Pousse le code sur GitHub :"
echo "   cd ~/gestion_etudiants"
echo "   git init"
echo "   git add ."
echo '   git commit -m "Gestion étudiants"'
echo "   git remote add origin https://github.com/toncompte/gestion-etudiants.git"
echo "   git push -u origin main"
echo ""
echo "6. Va sur https://share.streamlit.io"
echo "   → New app → choisis ton dépôt → Branch: main → File: streamlit_app.py"
echo ""
echo "7. Dans Streamlit Cloud → Settings → Secrets :"
echo '   Ajoute : MONGO_URI = "ton_uri_mongodb_atlas"'
echo ""
echo "8. Migre les données :"
echo "   python3 migrate_to_atlas.py \"ton_uri_mongodb_atlas\""
echo ""

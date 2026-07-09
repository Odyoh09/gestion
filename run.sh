#!/bin/bash
source "$(dirname "$0")/venv/bin/activate"
echo "=== Gestion des Étudiants - Interface Web ==="
echo "Démarrage du serveur sur http://localhost:5000"
echo ""
python3 "$(dirname "$0")/app.py"

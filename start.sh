#!/bin/bash

echo "========================================"
echo "  SEO Intelligence Suite Pro v6.0"
echo "  Démarrage de l'application..."
echo "========================================"
echo ""

# Activer l'environnement virtuel
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
    echo "[OK] Environnement virtuel activé"
else
    echo "[ERREUR] Environnement virtuel non trouvé"
    echo "Veuillez d'abord exécuter:"
    echo "  python3 -m venv venv"
    echo "  source venv/bin/activate"
    echo "  pip install -r requirements.txt"
    exit 1
fi

echo ""
echo "[INFO] Lancement de Streamlit..."
echo "[INFO] L'application va s'ouvrir dans votre navigateur"
echo "[INFO] URL: http://localhost:8501"
echo ""
echo "Appuyez sur Ctrl+C pour arrêter l'application"
echo ""

streamlit run main.py

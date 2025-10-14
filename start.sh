#!/bin/bash
# Script de démarrage rapide du Dashboard

echo "🚀 Démarrage du Dashboard Étudiant..."
echo ""

# Vérifier si le venv existe
if [ ! -d "venv" ]; then
    echo "❌ Environnement virtuel non trouvé. Création..."
    python3 -m venv venv
    echo "✅ Environnement virtuel créé"
fi

# Activer le venv et installer les dépendances
echo "📦 Installation des dépendances..."
source venv/bin/activate
pip install -q -r requirements.txt

echo "✅ Dépendances installées"
echo ""
echo "🌐 Lancement de l'application sur http://127.0.0.1:5001"
echo "   Appuyez sur CTRL+C pour arrêter"
echo ""

# Lancer l'application
python app.py

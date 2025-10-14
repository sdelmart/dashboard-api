#!/bin/bash
# Script d'arrêt du Dashboard

echo "🛑 Arrêt du Dashboard Étudiant..."
echo ""

# Chercher le processus Flask sur le port 5001
PID=$(lsof -ti:5001)

if [ -z "$PID" ]; then
    echo "ℹ️  Aucun serveur en cours d'exécution sur le port 5001"
else
    echo "🔍 Processus trouvé (PID: $PID)"
    kill $PID
    echo "✅ Serveur arrêté avec succès"
fi

echo ""
echo "✨ Terminé. Vous pouvez fermer cette fenêtre."
sleep 2

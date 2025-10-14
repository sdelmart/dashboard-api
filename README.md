# 📚 Dashboard Étudiant Personnel

Dashboard web pour améliorer la productivité étudiante au quotidien. Application Flask avec interface moderne et responsive.

## ✨ Fonctionnalités

### 1. ✅ Gestionnaire de Tâches
- Ajouter, supprimer et modifier des tâches
- Marquer les tâches comme complétées
- Définir des priorités (faible, moyenne, haute)
- Ajouter des dates d'échéance
- Stockage persistant en JSON

### 2. 🌤️ Météo
- Température et conditions actuelles
- Intégration avec OpenWeatherMap API
- Ville configurable (par défaut: Lyon)
- Ressenti et taux d'humidité

### 3. 🔗 Liens Rapides
- Accès rapide aux sites importants
- ENT, Moodle, GitLab, GitHub
- Gmail, Drive
- Configuration via JSON

### 4. 🎯 Objectifs Quotidiens
- Maximum 3 objectifs par jour
- Suivi de progression avec barre visuelle
- Réinitialisation automatique chaque jour
- Statistiques de complétion

### 5. ⏰ Rappels et Alertes
- Rappels pour examens, rendus, réunions
- Niveaux d'urgence automatiques selon les dates
- Indicateurs visuels (en retard, aujourd'hui, urgent, bientôt)
- Notifications par couleur

### 6. 📊 Statistiques
- Tâches complétées
- Objectifs atteints (pourcentage)
- Rappels urgents

## 🚀 Installation

### Prérequis
- Python 3.7+
- pip

### Installation des dépendances

```bash
pip install flask requests
```

Ou avec le venv existant:

```bash
cd "/Users/scott/Projets Persos/mon_dashboard"
source venv/bin/activate  # Sur macOS/Linux
pip install flask requests
```

## 🎮 Démarrage

### Méthode 1: Avec le venv

```bash
cd "/Users/scott/Projets Persos/mon_dashboard"
"/Users/scott/Projets Persos/mon_dashboard/venv/bin/python" app.py
```

### Méthode 2: Après activation du venv

```bash
cd "/Users/scott/Projets Persos/mon_dashboard"
source venv/bin/activate
python app.py
```

L'application sera accessible à l'adresse: **http://127.0.0.1:5001**

## ⚙️ Configuration

### Configuration de l'API Météo

1. Créez un compte gratuit sur [OpenWeatherMap](https://openweathermap.org/api)
2. Obtenez votre clé API
3. Modifiez le fichier `data/config.json`:

```json
{
  "weather": {
    "city": "Lyon",
    "openweathermap_api_key": "VOTRE_CLE_API_ICI"
  }
}
```

### Personnalisation des Liens Rapides

Modifiez `data/config.json` pour ajouter vos propres liens:

```json
{
  "quick_links": [
    {"name": "Mon Site", "url": "https://example.com"}
  ]
}
```

## 📁 Structure du Projet

```
mon_dashboard/
├── app.py                    # Application Flask principale
├── modules/
│   ├── todo_manager.py       # Gestion des tâches
│   ├── weather.py            # Service météo
│   ├── quick_links.py        # Gestion des liens
│   ├── daily_goals.py        # Objectifs quotidiens
│   └── reminders.py          # Système de rappels
├── data/
│   ├── tasks.json            # Stockage des tâches
│   ├── goals.json            # Stockage des objectifs
│   ├── reminders.json        # Stockage des rappels
│   └── config.json           # Configuration
├── templates/
│   ├── base.html             # Template de base
│   └── index.html            # Page principale
├── static/
│   └── style.css             # Styles CSS
└── README.md                 # Ce fichier
```

## 🔧 API REST

### Tâches
- `GET /api/todos` - Liste toutes les tâches
- `POST /api/todos` - Ajoute une tâche
- `PUT /api/todos/<id>` - Met à jour une tâche
- `DELETE /api/todos/<id>` - Supprime une tâche

### Météo
- `GET /api/weather` - Récupère la météo actuelle

### Liens Rapides
- `GET /api/links` - Liste les liens
- `POST /api/links` - Ajoute un lien

### Objectifs Quotidiens
- `GET /api/goals` - Liste les objectifs du jour
- `POST /api/goals` - Ajoute un objectif
- `POST /api/goals/<id>/toggle` - Marque comme complété
- `GET /api/goals/stats` - Statistiques

### Rappels
- `GET /api/reminders` - Liste les rappels
- `POST /api/reminders` - Ajoute un rappel
- `DELETE /api/reminders/<id>` - Supprime un rappel
- `POST /api/reminders/<id>/toggle` - Marque comme complété

## 🎨 Interface

- Design moderne et épuré
- Responsive (mobile, tablette, desktop)
- Grille adaptative
- Indicateurs visuels de priorité et d'urgence
- Animations et transitions fluides
- Thème bleu professionnel

## 📱 Responsive

L'application s'adapte automatiquement à toutes les tailles d'écran:
- Desktop: grille 3 colonnes
- Tablette: grille 2 colonnes
- Mobile: 1 colonne

## 🔒 Données

Toutes les données sont stockées localement dans des fichiers JSON:
- Pas de base de données requise
- Fichiers facilement éditables
- Sauvegarde automatique

## 🚧 Améliorations Futures

- [ ] Système de notifications push
- [ ] Mode sombre
- [ ] Export des données (PDF, CSV)
- [ ] Synchronisation cloud
- [ ] Application mobile
- [ ] Intégration calendrier
- [ ] Graphiques de productivité
- [ ] Thèmes personnalisables

## 📝 Notes

- Port par défaut: 5001 (modifiable dans app.py)
- Mode debug activé pour le développement
- Les objectifs se réinitialisent automatiquement chaque jour
- Les rappels calculent l'urgence automatiquement

## 🤝 Utilisation

1. Lancez l'application
2. Ouvrez http://127.0.0.1:5001 dans votre navigateur
3. Commencez à ajouter vos tâches, objectifs et rappels
4. Configurez votre clé API météo pour voir la météo

## 📄 Licence

Projet personnel - Libre d'utilisation

---

Développé avec ❤️ pour améliorer la productivité étudiante

"""Dashboard Personnel - Application Flask

Dashboard étudiant avec gestion de tâches, météo, liens rapides,
objectifs quotidiens et rappels.
"""
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from modules.todo_manager import TodoManager
from modules.weather import WeatherService
from modules.quick_links import QuickLinksManager
from modules.daily_goals import DailyGoalsManager
from modules.reminders import RemindersManager
import os
import json
from typing import Any

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, 'data')
TASKS_FILE = os.path.join(DATA_DIR, 'tasks.json')
GOALS_FILE = os.path.join(DATA_DIR, 'goals.json')
REMINDERS_FILE = os.path.join(DATA_DIR, 'reminders.json')
CONFIG_FILE = os.path.join(DATA_DIR, 'config.json')

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)  # Activer CORS pour permettre les requêtes depuis le portfolio

# Initialiser les gestionnaires
todo_mgr = TodoManager(TASKS_FILE)
goals_mgr = DailyGoalsManager(GOALS_FILE)
reminders_mgr = RemindersManager(REMINDERS_FILE)
links_mgr = QuickLinksManager(CONFIG_FILE)

# Charger la config pour la météo
def get_weather_config() -> dict[str, Any]:
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            config = json.load(f)
            return config.get('weather', {})
    except Exception:
        return {}

@app.route('/')
def index():
    """Page principale du dashboard."""
    return render_template('index.html')

# ============= ENDPOINTS TÂCHES =============
@app.route('/api/todos', methods=['GET'])
def api_get_todos():
    """Récupère toutes les tâches."""
    return jsonify(todo_mgr.list_tasks())

@app.route('/api/todos', methods=['POST'])
def api_add_todo():
    """Ajoute une nouvelle tâche."""
    data: dict[str, Any] = request.get_json() or {}
    title: str | None = data.get('title')
    if not title:
        return jsonify({'error': 'Titre requis'}), 400
    priority: str = data.get('priority', 'medium')
    due: str | None = data.get('due')
    task = todo_mgr.add_task(title=title, priority=priority, due=due)
    return jsonify(task), 201

@app.route('/api/todos/<task_id>', methods=['PUT'])
def api_update_todo(task_id: str):
    """Met à jour une tâche."""
    data: dict[str, Any] = request.get_json() or {}
    task = todo_mgr.update_task(task_id, data)
    if task is None:
        return jsonify({'error': 'Tâche non trouvée'}), 404
    return jsonify(task)

@app.route('/api/todos/<task_id>', methods=['DELETE'])
def api_delete_todo(task_id: str):
    """Supprime une tâche."""
    ok = todo_mgr.remove_task(task_id)
    if not ok:
        return jsonify({'error': 'Tâche non trouvée'}), 404
    return ('', 204)

# ============= ENDPOINTS MÉTÉO =============
@app.route('/api/weather', methods=['GET'])
def api_get_weather():
    """Récupère la météo actuelle."""
    config: dict[str, Any] = get_weather_config()
    api_key: str = config.get('openweathermap_api_key', '')
    city: str = config.get('city', 'Lyon')
    
    weather_service = WeatherService(api_key, city)
    data = weather_service.get_current_weather()
    return jsonify(data)

# ============= ENDPOINTS LIENS RAPIDES =============
@app.route('/api/links', methods=['GET'])
def api_get_links():
    """Récupère les liens rapides."""
    return jsonify(links_mgr.get_links())

@app.route('/api/links', methods=['POST'])
def api_add_link():
    """Ajoute un nouveau lien."""
    data: dict[str, Any] = request.get_json() or {}
    name: str | None = data.get('name')
    url: str | None = data.get('url')
    if not name or not url:
        return jsonify({'error': 'Nom et URL requis'}), 400
    ok = links_mgr.add_link(name, url)
    if ok:
        return jsonify({'name': name, 'url': url}), 201
    return jsonify({'error': 'Erreur lors de l\'ajout'}), 500

# ============= ENDPOINTS OBJECTIFS QUOTIDIENS =============
@app.route('/api/goals', methods=['GET'])
def api_get_goals():
    """Récupère les objectifs du jour."""
    return jsonify(goals_mgr.get_goals())

@app.route('/api/goals', methods=['POST'])
def api_add_goal():
    """Ajoute un nouvel objectif."""
    data: dict[str, Any] = request.get_json() or {}
    text: str | None = data.get('text')
    if not text:
        return jsonify({'error': 'Texte requis'}), 400
    goal = goals_mgr.add_goal(text)
    if 'error' in goal:
        return jsonify(goal), 400
    return jsonify(goal), 201

@app.route('/api/goals/<int:goal_id>/toggle', methods=['POST'])
def api_toggle_goal(goal_id: int):
    """Marque un objectif comme complété/non complété."""
    ok = goals_mgr.toggle_goal(goal_id)
    if not ok:
        return jsonify({'error': 'Objectif non trouvé'}), 404
    return jsonify({'success': True})

@app.route('/api/goals/stats', methods=['GET'])
def api_get_goal_stats():
    """Récupère les statistiques des objectifs."""
    return jsonify(goals_mgr.get_stats())

# ============= ENDPOINTS RAPPELS =============
@app.route('/api/reminders', methods=['GET'])
def api_get_reminders():
    """Récupère tous les rappels."""
    return jsonify(reminders_mgr.list_reminders())

@app.route('/api/reminders', methods=['POST'])
def api_add_reminder():
    """Ajoute un nouveau rappel."""
    data: dict[str, Any] = request.get_json() or {}
    title: str | None = data.get('title')
    due_date: str | None = data.get('due_date')
    reminder_type: str = data.get('type', 'general')
    
    if not title or not due_date:
        return jsonify({'error': 'Titre et date requis'}), 400
    
    reminder = reminders_mgr.add_reminder(title, due_date, reminder_type)
    return jsonify(reminder), 201

@app.route('/api/reminders/<reminder_id>', methods=['DELETE'])
def api_delete_reminder(reminder_id: str):
    """Supprime un rappel."""
    ok = reminders_mgr.remove_reminder(reminder_id)
    if not ok:
        return jsonify({'error': 'Rappel non trouvé'}), 404
    return ('', 204)

@app.route('/api/reminders/<reminder_id>/toggle', methods=['POST'])
def api_toggle_reminder(reminder_id: str):
    """Marque un rappel comme complété/non complété."""
    reminder = reminders_mgr.toggle_reminder(reminder_id)
    if reminder is None:
        return jsonify({'error': 'Rappel non trouvé'}), 404
    return jsonify(reminder)

if __name__ == '__main__':
    app.run(debug=True, port=5001)

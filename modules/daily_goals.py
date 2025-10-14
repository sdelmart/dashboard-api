"""Daily Goals Manager - Gestion des objectifs quotidiens

Permet de définir et suivre jusqu'à 3 objectifs par jour.
Auto-reset à minuit.
"""
import json
import os
from datetime import date
from typing import Dict, Any


class DailyGoalsManager:
    def __init__(self, filepath: str):
        self.filepath = filepath
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        if not os.path.exists(self.filepath) or os.path.getsize(self.filepath) == 0:
            self._write({'date': str(date.today()), 'goals': []})

    def _read(self) -> Dict[str, Any]:
        with open(self.filepath, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _write(self, data: Dict[str, Any]):
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def _check_and_reset(self) -> Dict[str, Any]:
        """Réinitialise les objectifs si on est un nouveau jour."""
        data : Dict[str, Any]
        data = self._read()
        today = str(date.today())
        if data.get('date') != today:
            data = {'date': today, 'goals': []}
            self._write(data)
        return data

    def get_goals(self) -> Dict[str, Any]:
        """Retourne les objectifs du jour."""
        return self._check_and_reset()

    def add_goal(self, text: str) -> Dict[str, Any]:
        """Ajoute un nouvel objectif (max 3)."""
        goal: Dict[str, Any]
        data = self._check_and_reset()
        if len(data['goals']) >= 3:
            return {'error': 'Maximum 3 objectifs par jour'}
        
        goal = {
            'id': len(data['goals']) + 1,
            'text': text,
            'completed': False
        }
        data['goals'].append(goal)
        self._write(data)
        return goal

    def toggle_goal(self, goal_id: int) -> bool:
        """Inverse l'état d'un objectif."""
        data = self._check_and_reset()
        for goal in data['goals']:
            if goal['id'] == goal_id:
                goal['completed'] = not goal['completed']
                self._write(data)
                return True
        return False

    def get_stats(self) -> Dict[str, Any]:
        """Retourne les statistiques."""
        data = self._check_and_reset()
        total = len(data['goals'])
        completed = sum(1 for g in data['goals'] if g['completed'])
        return {
            'total': total,
            'completed': completed,
            'percentage': round((completed / total * 100) if total > 0 else 0, 1)
        }

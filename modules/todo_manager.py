"""Gestionnaire de tâches avec stockage JSON.

Fonctionnalités:
- Ajouter des tâches
- Supprimer des tâches
- Marquer comme complétées
- Définir des priorités (faible, moyenne, haute)
- Dates d'échéance optionnelles
"""
from typing import List, Optional, Dict, Any
import json
import os
import uuid
from datetime import datetime, timezone


class TodoManager:
    def __init__(self, filepath: str):
        self.filepath = filepath
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        if not os.path.exists(filepath) or os.path.getsize(filepath) == 0:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump([], f)

    def _read(self) -> List[Dict[str, Any]]:
        with open(self.filepath, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _write(self, tasks: List[Dict[str, Any]]):
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump(tasks, f, ensure_ascii=False, indent=2)

    def list_tasks(self) -> List[Dict[str, Any]]:
        """Retourne toutes les tâches."""
        return self._read()

    def add_task(self, title: str, priority: str = 'medium', due: Optional[str] = None) -> Dict[str, Any]:
        """Ajoute une nouvelle tâche."""
        new_task: Dict[str, Any]
        tasks = self._read()
        new_task = {
            'id': str(uuid.uuid4()),
            'title': title,
            'completed': False,
            'priority': priority if priority in ('low', 'medium', 'high') else 'medium',
            'due': due,
            'created_at': datetime.now(timezone.utc).isoformat()
        }
        tasks.append(new_task)
        self._write(tasks)
        return new_task

    def remove_task(self, task_id: str) -> bool:
        """Supprime une tâche par ID."""
        tasks = self._read()
        new_tasks = [t for t in tasks if t.get('id') != task_id]
        if len(new_tasks) == len(tasks):
            return False
        self._write(new_tasks)
        return True

    def update_task(self, task_id: str, fields: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Met à jour une tâche."""
        tasks = self._read()
        for t in tasks:
            if t.get('id') == task_id:
                if 'title' in fields:
                    t['title'] = fields['title']
                if 'completed' in fields:
                    t['completed'] = bool(fields['completed'])
                if 'priority' in fields and fields['priority'] in ('low', 'medium', 'high'):
                    t['priority'] = fields['priority']
                if 'due' in fields:
                    t['due'] = fields['due']
                t['updated_at'] = datetime.now(timezone.utc).isoformat()
                self._write(tasks)
                return t
        return None

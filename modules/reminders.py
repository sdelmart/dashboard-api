"""Reminders Manager - Gestion des rappels

Système de rappels avec calcul automatique d'urgence
basé sur les dates d'échéance.
"""
import json
import os
import uuid
from datetime import datetime, date
from typing import List, Dict, Any, Optional


class RemindersManager:
    def __init__(self, filepath: str):
        self.filepath = filepath
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        if not os.path.exists(filepath) or os.path.getsize(filepath) == 0:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump([], f)

    def _read(self) -> List[Dict[str, Any]]:
        with open(self.filepath, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _write(self, reminders: List[Dict[str, Any]]):
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump(reminders, f, ensure_ascii=False, indent=2)

    def _calculate_urgency(self, due_date: str) -> str:
        """Calcule le niveau d'urgence selon la date."""
        try:
            due = datetime.fromisoformat(due_date).date()
            today = date.today()
            delta = (due - today).days
            
            if delta < 0:
                return 'overdue'
            elif delta == 0:
                return 'today'
            elif delta <= 1:
                return 'urgent'
            elif delta <= 7:
                return 'soon'
            else:
                return 'normal'
        except Exception:
            return 'normal'

    def list_reminders(self) -> List[Dict[str, Any]]:
        """Retourne tous les rappels avec urgence calculée."""
        reminders = self._read()
        for r in reminders:
            if r.get('due_date'):
                r['urgency'] = self._calculate_urgency(r['due_date'])
        # Trier par urgence et date
        urgency_order = {'overdue': 0, 'today': 1, 'urgent': 2, 'soon': 3, 'normal': 4}
        reminders.sort(key=lambda x: (urgency_order.get(x.get('urgency', 'normal'), 5), x.get('due_date', '')))
        return reminders

    def add_reminder(self, title: str, due_date: str, reminder_type: str = 'general') -> Dict[str, Any]:
        """Ajoute un nouveau rappel."""
        new_reminder: Dict[str, Any]
        reminders = self._read()
        new_reminder = {
            'id': str(uuid.uuid4()),
            'title': title,
            'due_date': due_date,
            'type': reminder_type,  # exam, assignment, meeting, general
            'urgency': self._calculate_urgency(due_date),
            'completed': False
        }
        reminders.append(new_reminder)
        self._write(reminders)
        return new_reminder

    def remove_reminder(self, reminder_id: str) -> bool:
        """Supprime un rappel."""
        reminders = self._read()
        new_reminders = [r for r in reminders if r.get('id') != reminder_id]
        if len(new_reminders) == len(reminders):
            return False
        self._write(new_reminders)
        return True

    def toggle_reminder(self, reminder_id: str) -> Optional[Dict[str, Any]]:
        """Marque un rappel comme complété/non complété."""
        reminders = self._read()
        for r in reminders:
            if r.get('id') == reminder_id:
                r['completed'] = not r.get('completed', False)
                self._write(reminders)
                return r
        return None

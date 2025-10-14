"""Quick Links Manager - Gestion des liens rapides

Gère une liste de liens favoris configurables.
"""
import json
import os
from typing import List, Dict, cast


class QuickLinksManager:
    def __init__(self, config_path: str):
        self.config_path = config_path

    def get_links(self) -> List[Dict[str, str]]:
        """Retourne la liste des liens rapides."""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    raw = json.load(f)
                    config = cast(Dict[str, List[Dict[str, str]]], raw)
                    return config.get('quick_links', [])
            return []
        except Exception:
            return []
    def add_link(self, name: str, url: str) -> bool:
        """Ajoute un nouveau lien."""
        try:
            # typed config to help static analyzers understand the structure
            config: Dict[str, List[Dict[str, str]]] = {}
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    raw = json.load(f)
                    config = cast(Dict[str, List[Dict[str, str]]], raw)
            
            if 'quick_links' not in config:
                config['quick_links'] = []
            
            config['quick_links'].append({'name': name, 'url': url})
            
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            return True
        except Exception:
            return False
            return False

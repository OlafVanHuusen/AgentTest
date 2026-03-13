import json
import os
from pathlib import Path


class LoreLoader:
    def __init__(self, lore_dir: str = None):
        if lore_dir is None:
            lore_dir = Path(__file__).parent
        self.lore_dir = Path(lore_dir)
        self._npcs = None
        self._setting = None
        self._endings = None

    @property
    def npcs(self):
        if self._npcs is None:
            with open(self.lore_dir / "npcs.json") as f:
                self._npcs = json.load(f)
        return self._npcs

    @property
    def setting(self):
        if self._setting is None:
            with open(self.lore_dir / "setting.json") as f:
                self._setting = json.load(f)
        return self._setting

    @property
    def endings(self):
        if self._endings is None:
            with open(self.lore_dir / "endings.json") as f:
                self._endings = json.load(f)
        return self._endings

    def get_npc(self, name: str):
        for npc in self.npcs.get("npcs", []):
            if npc.get("name", "").lower() == name.lower():
                return npc
        return None

    def get_setting(self):
        return self.setting

    def get_ending(self, ending_id: str):
        for ending in self.endings.get("endings", []):
            if ending.get("id") == ending_id:
                return ending
        return None
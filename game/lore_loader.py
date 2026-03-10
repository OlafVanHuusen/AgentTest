import json
import os
from pathlib import Path


class LoreLoader:
    def __init__(self, lore_dir: str = None):
        if lore_dir is None:
            base_dir = Path(__file__).parent.parent
            lore_dir = base_dir / "lore"
        self.lore_dir = Path(lore_dir)
        self._npcs = None
        self._setting = None
        self._endings = None

    def load_npcs(self) -> dict:
        if self._npcs is None:
            npcs_path = self.lore_dir / "npcs.json"
            with open(npcs_path, "r", encoding="utf-8") as f:
                self._npcs = json.load(f)
        return self._npcs

    def load_setting(self) -> dict:
        if self._setting is None:
            setting_path = self.lore_dir / "setting.json"
            with open(setting_path, "r", encoding="utf-8") as f:
                self._setting = json.load(f)
        return self._setting

    def load_endings(self) -> dict:
        if self._endings is None:
            endings_path = self.lore_dir / "endings.json"
            with open(endings_path, "r", encoding="utf-8") as f:
                self._endings = json.load(f)
        return self._endings

    def get_npc(self, npc_id: str) -> dict:
        npcs = self.load_npcs()
        return npcs.get(npc_id)

    def get_ending(self, ending_id: str) -> dict:
        endings = self.load_endings()
        return endings.get(ending_id)

    def get_all_lore(self) -> dict:
        return {
            "npcs": self.load_npcs(),
            "setting": self.load_setting(),
            "endings": self.load_endings(),
        }


_lore_loader = None


def get_lore_loader() -> LoreLoader:
    global _lore_loader
    if _lore_loader is None:
        _lore_loader = LoreLoader()
    return _lore_loader

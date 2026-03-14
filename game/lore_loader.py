import json
import logging
import os
from pathlib import Path
from typing import Optional, Union


logger = logging.getLogger(__name__)


class LoreLoader:
    def __init__(self, lore_dir: Union[str, Path, None] = None):
        if lore_dir is None:
            base_dir = Path(__file__).parent.parent
            lore_dir = base_dir / "lore"
        self.lore_dir = Path(lore_dir)
        self._npcs: Optional[dict] = None
        self._setting: Optional[dict] = None
        self._endings: Optional[dict] = None

    def _load_json(self, filename: str) -> Optional[dict]:
        path = self.lore_dir / filename
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning(f"Lore file not found: {path}")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in {path}: {e}")
            return None

    def load_npcs(self) -> dict:
        if self._npcs is None:
            self._npcs = self._load_json("npcs.json")
            if self._npcs is None:
                self._npcs = {}
        return self._npcs

    def load_setting(self) -> dict:
        if self._setting is None:
            self._setting = self._load_json("setting.json")
            if self._setting is None:
                self._setting = {}
        return self._setting

    def load_endings(self) -> dict:
        if self._endings is None:
            self._endings = self._load_json("endings.json")
            if self._endings is None:
                self._endings = {}
        return self._endings

    def get_npc(self, npc_id: str) -> Optional[dict]:
        npcs = self.load_npcs()
        return npcs.get(npc_id)

    def get_ending(self, ending_id: str) -> Optional[dict]:
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

import json
import logging
import os
from pathlib import Path
from typing import Optional, Union

import config


logger = logging.getLogger(__name__)

EMBEDDED_NPCS = {
    "driver": {
        "name": "Driver",
        "description": "A silent driver with mysterious goggles. They never speak, but their eyes constantly check the rearview mirror.",
        "behavior": "drives_silently"
    },
    "business": {
        "name": "Business Person",
        "description": "Immaculately dressed, constantly checking their phone. Seeks efficiency above all.",
        "behavior": "impatient"
    },
    "elderly": {
        "name": "Elderly Woman",
        "description": "A kind grandmother type who reminisces about the 'old bus routes'. Seems to know more than she lets on.",
        "behavior": "reminisces"
    },
    "teen": {
        "name": "Teenager",
        "description": "Wearing headphones, nodding to invisible music. The loop seems to affect them differently.",
        "behavior": "oblivious"
    }
}

EMBEDDED_SETTING = {
    "name": "Timeloop Bus",
    "atmosphere": "A cramped 1980s city bus trapped in an infinite time loop. The overhead lights flicker. Rain hammers the windows.",
    "rules": [
        "The bus loops back every 10 minutes",
        "Every passenger has a secret",
        "The driver never speaks",
        "Some passengers remember previous loops"
    ],
    "visual_elements": [
        "Flickering overhead lights",
        "Rain-streaked windows",
        "Worn seats",
        "Poster for 'Cascade Tours' company"
    ]
}

EMBEDDED_ENDINGS = {
    "good": {
        "id": "good",
        "title": "The Last Stop",
        "description": "You helped all passengers confront their secrets. The bus doors open to a sunrise. You step out into a new day.",
        "condition": "All passengers helped"
    },
    "bad": {
        "id": "bad", 
        "title": "Lost in the Loop",
        "description": "You couldn't break the cycle. The bus keeps driving, forever. The driver smiles in the rearview mirror.",
        "condition": "Failed to help passengers"
    },
    "secret": {
        "id": "secret",
        "title": "The Driver's Secret",
        "description": "You discovered the truth - you ARE the driver. The goggles fall off. Your face stares back at you.",
        "condition": "Investigated the driver"
    }
}


class LoreLoader:
    def __init__(self, lore_dir: Union[str, Path, None] = None):
        if lore_dir is None:
            base_dir = Path(__file__).parent.parent
            lore_dir = base_dir / "lore"
        self.lore_dir = Path(lore_dir)
        self._npcs: Optional[dict] = None
        self._setting: Optional[dict] = None
        self._endings: Optional[dict] = None
        self._web_mode = getattr(config, 'WEB_MODE', False)

    def _load_json(self, filename: str) -> Optional[dict]:
        if self._web_mode:
            return None
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
            data = self._load_json("npcs.json")
            if data is None:
                data = {"npcs": list(EMBEDDED_NPCS.values())}
            self._npcs = data
        return self._npcs

    def load_setting(self) -> dict:
        if self._setting is None:
            data = self._load_json("setting.json")
            if data is None:
                data = EMBEDDED_SETTING
            self._setting = data
        return self._setting

    def load_endings(self) -> dict:
        if self._endings is None:
            data = self._load_json("endings.json")
            if data is None:
                data = {"endings": list(EMBEDDED_ENDINGS.values())}
            self._endings = data
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

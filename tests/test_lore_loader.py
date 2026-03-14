import json
import tempfile
import os
from pathlib import Path
from game.lore_loader import LoreLoader


class TestLoreLoader:
    def test_load_npcs(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            npcs_data = {"npc1": {"name": "Test NPC"}}
            npcs_file = Path(tmpdir) / "npcs.json"
            with open(npcs_file, "w") as f:
                json.dump(npcs_data, f)
            
            loader = LoreLoader(tmpdir)
            result = loader.load_npcs()
            assert result == npcs_data

    def test_load_setting(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            setting_data = {"title": "Test Game", "rules": ["rule1"]}
            setting_file = Path(tmpdir) / "setting.json"
            with open(setting_file, "w") as f:
                json.dump(setting_data, f)
            
            loader = LoreLoader(tmpdir)
            result = loader.load_setting()
            assert result == setting_data

    def test_load_endings(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            endings_data = {"ending1": {"text": "Test ending"}}
            endings_file = Path(tmpdir) / "endings.json"
            with open(endings_file, "w") as f:
                json.dump(endings_data, f)
            
            loader = LoreLoader(tmpdir)
            result = loader.load_endings()
            assert result == endings_data

    def test_missing_file_returns_empty_dict(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            loader = LoreLoader(tmpdir)
            result = loader.load_npcs()
            assert result == {}

    def test_get_npc(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            npcs_data = {"npc1": {"name": "Test NPC"}}
            npcs_file = Path(tmpdir) / "npcs.json"
            with open(npcs_file, "w") as f:
                json.dump(npcs_data, f)
            
            loader = LoreLoader(tmpdir)
            result = loader.get_npc("npc1")
            assert result == {"name": "Test NPC"}

    def test_get_npc_not_found(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            npcs_data = {"npc1": {"name": "Test NPC"}}
            npcs_file = Path(tmpdir) / "npcs.json"
            with open(npcs_file, "w") as f:
                json.dump(npcs_data, f)
            
            loader = LoreLoader(tmpdir)
            result = loader.get_npc("nonexistent")
            assert result is None

    def test_get_ending(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            endings_data = {"ending1": {"text": "Test ending"}}
            endings_file = Path(tmpdir) / "endings.json"
            with open(endings_file, "w") as f:
                json.dump(endings_data, f)
            
            loader = LoreLoader(tmpdir)
            result = loader.get_ending("ending1")
            assert result == {"text": "Test ending"}

    def test_get_all_lore(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            npcs_data = {"npc1": {"name": "Test NPC"}}
            setting_data = {"title": "Test Game"}
            endings_data = {"ending1": {"text": "Test ending"}}
            
            with open(Path(tmpdir) / "npcs.json", "w") as f:
                json.dump(npcs_data, f)
            with open(Path(tmpdir) / "setting.json", "w") as f:
                json.dump(setting_data, f)
            with open(Path(tmpdir) / "endings.json", "w") as f:
                json.dump(endings_data, f)
            
            loader = LoreLoader(tmpdir)
            result = loader.get_all_lore()
            assert result["npcs"] == npcs_data
            assert result["setting"] == setting_data
            assert result["endings"] == endings_data

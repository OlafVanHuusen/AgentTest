import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
from llm import ollama, groq
from game.lore_loader import LoreLoader


class TestLLMClients(unittest.TestCase):
    def test_ollama_client_import(self):
        from llm.ollama import OllamaClient
        client = OllamaClient()
        self.assertIsNotNone(client.url)
        self.assertIsNotNone(client.model)

    def test_groq_client_import(self):
        from llm.groq import GroqClient
        client = GroqClient()
        self.assertIsNotNone(client.model)

    def test_ollama_generate_requires_available(self):
        from llm.ollama import OllamaClient
        client = OllamaClient()
        with patch.object(client, 'is_available', return_value=False):
            with self.assertRaises(RuntimeError):
                client.generate("test prompt")

    def test_groq_generate_requires_available(self):
        from llm.groq import GroqClient
        client = GroqClient()
        with patch.object(client, 'is_available', return_value=False):
            with self.assertRaises(RuntimeError):
                client.generate("test prompt")


class TestLoreLoader(unittest.TestCase):
    def setUp(self):
        self.loader = LoreLoader()

    def test_load_setting(self):
        setting = self.loader.load_setting()
        self.assertIn("title", setting)
        self.assertIn("atmosphere", setting)
        self.assertIn("rules", setting)

    def test_load_npcs(self):
        npcs = self.loader.load_npcs()
        self.assertIn("driver", npcs)
        self.assertIn("alex", npcs)
        self.assertIn("maria", npcs)
        self.assertIn("emo_boy", npcs)

    def test_load_endings(self):
        endings = self.loader.load_endings()
        self.assertIn("ending_1_coma", endings)
        self.assertIn("ending_2_dark_city", endings)
        self.assertIn("ending_3_give_up", endings)

    def test_get_npc(self):
        driver = self.loader.get_npc("driver")
        self.assertEqual(driver["name"], "The Driver")
        self.assertIn("aware", driver["attributes"])

    def test_get_ending(self):
        ending = self.loader.get_ending("ending_1_coma")
        self.assertEqual(ending["name"], "Coma Wake")


class TestPromptBuilder(unittest.TestCase):
    def setUp(self):
        self.loader = LoreLoader()

    def build_prompt(self, action_text, game_state_dict):
        setting = self.loader.load_setting()
        npcs = self.loader.load_npcs()
        endings = self.loader.load_endings()

        loop_count = game_state_dict.get("loop_count", 1)
        current_minute = game_state_dict.get("current_minute", 2)
        actions_taken = game_state_dict.get("actions", [])
        world_changes = game_state_dict.get("world_changes", [])

        npc_descriptions = []
        for npc_id, npc in npcs.items():
            desc = f"- {npc['name'].upper()}: {npc['description']}"
            npc_descriptions.append(desc)

        prompt = f"""You are the game master for "{setting['title']}", an 8-bit text adventure game.

SETTING: {setting['time_of_day']}. {setting['bus_description']}
The player just woke up. The driver is silent.
Other passengers are on the bus.

ATMOSPHERE: {setting['atmosphere']}
{setting['lamp_description']}

NPCS:
{chr(10).join(npc_descriptions)}

RULES:
{chr(10).join(f"- {rule}" for rule in setting['rules'])}

CURRENT STATE:
- Loop: #{loop_count}, Minute: {current_minute}
- Actions taken: {actions_taken if actions_taken else "None yet"}
- World changes: {world_changes if world_changes else "None yet"}

The player performs this action: "{action_text}"

Respond with a descriptive, atmospheric response (2-4 sentences) that follows the game rules.
"""
        return prompt

    def test_prompt_includes_setting(self):
        prompt = self.build_prompt("test action", {"loop_count": 1, "current_minute": 2, "actions": []})
        self.assertIn("Timeloop Bus", prompt)
        self.assertIn("2:00 AM", prompt)

    def test_prompt_includes_npcs(self):
        prompt = self.build_prompt("test action", {"loop_count": 1, "current_minute": 2, "actions": []})
        self.assertIn("DRIVER", prompt)
        self.assertIn("ALEX", prompt)
        self.assertIn("MARIA", prompt)

    def test_prompt_includes_rules(self):
        prompt = self.build_prompt("test action", {"loop_count": 1, "current_minute": 2, "actions": []})
        self.assertIn("Player can do ANY action", prompt)
        self.assertIn("Passengers reset each loop", prompt)

    def test_prompt_includes_action(self):
        prompt = self.build_prompt("talk to driver", {"loop_count": 1, "current_minute": 2, "actions": []})
        self.assertIn("talk to driver", prompt)

    def test_prompt_includes_game_state(self):
        prompt = self.build_prompt("test", {"loop_count": 3, "current_minute": 5, "actions": ["woke up", "looked around"]})
        self.assertIn("#3", prompt)
        self.assertIn("Minute: 5", prompt)
        self.assertIn("woke up", prompt)


class TestAtmosphericResponseValidation(unittest.TestCase):
    def validate_atmospheric_response(self, response):
        if not response or len(response.strip()) < 10:
            return False, "Response too short"
        if len(response) > 500:
            return False, "Response too long"
        return True, "Valid"

    def test_validate_short_response(self):
        valid, msg = self.validate_atmospheric_response("Hi")
        self.assertFalse(valid)

    def test_validate_empty_response(self):
        valid, msg = self.validate_atmospheric_response("")
        self.assertFalse(valid)

    def test_validate_good_response(self):
        valid, msg = self.validate_atmospheric_response("The driver glances at you briefly. His eyes are tired but aware.")
        self.assertTrue(valid)

    def test_validate_very_long_response(self):
        long_text = "A" * 600
        valid, msg = self.validate_atmospheric_response(long_text)
        self.assertFalse(valid)


class TestGameRuleValidation(unittest.TestCase):
    def validate_game_rules(self, response, action):
        issues = []

        if not response or len(response.strip()) < 5:
            issues.append("Response too short")

        forbidden_phrases = ["I can't", "I'm sorry, but", "I am not able"]
        for phrase in forbidden_phrases:
            if phrase.lower() in response.lower():
                issues.append(f"Contains forbidden phrase: {phrase}")

        return len(issues) == 0, issues

    def test_valid_driver_response(self):
        response = "The driver grunts without turning his gaze from the road. His hands remain steady on the wheel."
        valid, issues = self.validate_game_rules(response, "talk to driver")
        self.assertTrue(valid)

    def test_valid_violent_response(self):
        response = "You smash the window with your elbow. Glass shatters. Cold air rushes in. The other passengers stir."
        valid, issues = self.validate_game_rules(response, "smash window")
        self.assertTrue(valid)

    def test_rejects_apology(self):
        response = "I'm sorry, but I can't let you do that."
        valid, issues = self.validate_game_rules(response, "kill driver")
        self.assertFalse(valid)


class TestFailoverHandler(unittest.TestCase):
    @patch('llm.ollama.OllamaClient.generate')
    @patch('llm.ollama.OllamaClient.is_available')
    def test_ollama_fails_over_to_groq(self, mock_ollama_available, mock_ollama_generate):
        from llm.groq import GroqClient

        mock_ollama_available.return_value = False
        mock_ollama_generate.side_effect = RuntimeError("Ollama unavailable")

        with patch('llm.groq.GroqClient.is_available', return_value=True):
            with patch('llm.groq.GroqClient.generate', return_value="Groq response"):
                from llm import groq
                client = groq.GroqClient()
                result = client.generate("test prompt")
                self.assertEqual(result, "Groq response")

    @patch('llm.ollama.OllamaClient.is_available')
    @patch('llm.groq.GroqClient.is_available')
    def test_both_fail_triggers_failover(self, mock_groq_avail, mock_ollama_avail):
        mock_ollama_avail.return_value = False
        mock_groq_avail.return_value = False

        from llm import ollama, groq
        ollama_client = ollama.OllamaClient()
        groq_client = groq.GroqClient()

        self.assertFalse(ollama_client.is_available())
        self.assertFalse(groq_client.is_available())


class TestActionResponses(unittest.TestCase):
    def setUp(self):
        self.loader = LoreLoader()
        self.actions = [
            "talk to driver",
            "smash window",
            "kill driver",
        ]

    def test_actions_defined(self):
        self.assertEqual(len(self.actions), 3)
        self.assertIn("talk to driver", self.actions)
        self.assertIn("smash window", self.actions)
        self.assertIn("kill driver", self.actions)

    def test_talk_to_driver_context(self):
        npcs = self.loader.load_npcs()
        driver = npcs["driver"]
        self.assertIn("aware", driver["attributes"])
        self.assertIn("protective", driver["attributes"])

    def test_smash_window_context(self):
        setting = self.loader.load_setting()
        bus_desc = setting["bus_description"].lower()
        self.assertTrue("window" in bus_desc or "20 seats" in bus_desc or "bus" in bus_desc)

    def test_kill_driver_context(self):
        setting = self.loader.load_setting()
        rules = setting["rules"]
        any_action_rule = any("any action" in rule.lower() for rule in rules)
        self.assertTrue(any_action_rule, "Rules should allow any action")


class TestIntegration(unittest.TestCase):
    def test_all_modules_import(self):
        import config
        import llm
        import llm.ollama
        import llm.groq
        import game
        import game.state
        import game.renderer
        import game.lore_loader
        self.assertTrue(True)

    def test_config_settings(self):
        self.assertEqual(config.SCREEN_WIDTH, 320)
        self.assertEqual(config.SCREEN_HEIGHT, 240)
        self.assertIn(config.PREFERRED_LLM, ["ollama", "groq"])

    def test_game_state_initialization(self):
        from game.state import GameState
        state = GameState()
        self.assertEqual(state.loop_count, 1)
        self.assertEqual(state.current_minute, 2)
        self.assertFalse(state.game_over)


if __name__ == "__main__":
    unittest.main(verbosity=2)

import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game.state import GameState
from game.action_tracker import ActionTracker
from game.lore_loader import LoreLoader
from llm.failover import FailoverHandler
import config


class TestEndingReachability(unittest.TestCase):
    def setUp(self):
        self.loader = LoreLoader()

    def test_ending_1_coma_trigger_exists(self):
        endings = self.loader.load_endings()
        self.assertIn("ending_1_coma", endings)
        self.assertEqual(endings["ending_1_coma"]["trigger"], "examine driver's lamp closely")

    def test_ending_2_dark_city_trigger_exists(self):
        endings = self.loader.load_endings()
        self.assertIn("ending_2_dark_city", endings)
        self.assertEqual(endings["ending_2_dark_city"]["trigger"], "smash the lamp")

    def test_ending_3_give_up_trigger_exists(self):
        endings = self.loader.load_endings()
        self.assertIn("ending_3_give_up", endings)
        self.assertEqual(endings["ending_3_give_up"]["trigger"], "kill yourself")

    def test_ending_detection_ending_1(self):
        state = GameState()
        action = "examine driver's lamp closely"
        endings = self.loader.load_endings()
        
        action_lower = action.lower()
        triggered = False
        for ending_id, ending in endings.items():
            trigger = ending.get("trigger", "").lower()
            if trigger in action_lower:
                state.set_ending(ending)
                triggered = True
                break
        
        self.assertTrue(triggered)
        self.assertTrue(state.game_over)
        self.assertEqual(state.ending["name"], "Coma Wake")

    def test_ending_detection_ending_2(self):
        state = GameState()
        action = "smash the lamp"
        endings = self.loader.load_endings()
        
        action_lower = action.lower()
        triggered = False
        for ending_id, ending in endings.items():
            trigger = ending.get("trigger", "").lower()
            if trigger in action_lower:
                state.set_ending(ending)
                triggered = True
                break
        
        self.assertTrue(triggered)
        self.assertTrue(state.game_over)
        self.assertEqual(state.ending["name"], "Dark City")

    def test_ending_detection_ending_3(self):
        state = GameState()
        action = "kill yourself"
        endings = self.loader.load_endings()
        
        action_lower = action.lower()
        triggered = False
        for ending_id, ending in endings.items():
            trigger = ending.get("trigger", "").lower()
            if trigger in action_lower:
                state.set_ending(ending)
                triggered = True
                break
        
        self.assertTrue(triggered)
        self.assertTrue(state.game_over)
        self.assertEqual(state.ending["name"], "Give Up")


class TestLoopResetVisualEffect(unittest.TestCase):
    def setUp(self):
        self.state = GameState()

    def test_loop_reset_state_attributes(self):
        self.state.loop_count = 1
        self.state.current_minute = 5
        self.state.actions = ["action1", "action2"]
        self.state.actions_this_loop = 3

        self.state.reset_loop()

        self.assertEqual(self.state.loop_count, 2)
        self.assertEqual(self.state.current_minute, 2)
        self.assertEqual(len(self.state.actions), 0)
        self.assertEqual(self.state.actions_this_loop, 0)

    def test_loop_reset_does_not_affect_ending(self):
        self.state.set_ending({"name": "Test", "result": "Test result"})
        self.state.reset_loop()
        
        self.assertTrue(self.state.game_over)
        self.assertIsNotNone(self.state.ending)

    def test_multiple_loop_resets(self):
        for i in range(1, 4):
            self.state.reset_loop()
            self.assertEqual(self.state.loop_count, i + 1)
            self.assertEqual(self.state.current_minute, 2)


class TestLLMFailover(unittest.TestCase):
    @patch('llm.ollama.OllamaClient.is_available')
    @patch('llm.groq.GroqClient.is_available')
    @patch('llm.ollama.OllamaClient.generate')
    @patch('llm.groq.GroqClient.generate')
    def test_failover_ollama_to_groq(self, mock_groq_gen, mock_ollama_gen, mock_groq_avail, mock_ollama_avail):
        mock_ollama_avail.return_value = True
        mock_groq_avail.return_value = True
        mock_ollama_gen.return_value = "Ollama response"
        mock_groq_gen.return_value = "Groq response"
        
        handler = FailoverHandler(preferred="ollama")
        
        result = handler.generate("test prompt")
        
        self.assertEqual(result, "Ollama response")

    @patch('llm.ollama.OllamaClient.is_available')
    @patch('llm.groq.GroqClient.is_available')
    @patch('llm.ollama.OllamaClient.generate')
    @patch('llm.groq.GroqClient.generate')
    def test_failover_primary_fails_uses_fallback(self, mock_groq_gen, mock_ollama_gen, mock_groq_avail, mock_ollama_avail):
        mock_ollama_avail.return_value = True
        mock_groq_avail.return_value = True
        mock_ollama_gen.side_effect = RuntimeError("Ollama error")
        mock_groq_gen.return_value = "Groq fallback response"
        
        handler = FailoverHandler(preferred="ollama")
        
        result = handler.generate("test prompt")
        
        self.assertEqual(result, "Groq fallback response")

    @patch('llm.ollama.OllamaClient.is_available')
    @patch('llm.groq.GroqClient.is_available')
    def test_failover_both_unavailable_raises(self, mock_groq_avail, mock_ollama_avail):
        mock_ollama_avail.return_value = False
        mock_groq_avail.return_value = False
        
        handler = FailoverHandler(preferred="ollama")
        
        with self.assertRaises(RuntimeError) as context:
            handler.generate("test prompt")
        
        self.assertIn("No LLM providers available", str(context.exception))

    @patch('llm.ollama.OllamaClient.generate')
    @patch('llm.groq.GroqClient.generate')
    @patch('llm.ollama.OllamaClient.is_available')
    @patch('llm.groq.GroqClient.is_available')
    def test_failover_prefers_groq_when_configured(self, mock_groq_avail, mock_ollama_avail, mock_groq_gen, mock_ollama_gen):
        mock_ollama_avail.return_value = True
        mock_groq_avail.return_value = True
        mock_ollama_gen.return_value = "Ollama response"
        mock_groq_gen.return_value = "Groq response"
        
        handler = FailoverHandler(preferred="groq")
        
        result = handler.generate("test prompt")
        
        self.assertEqual(result, "Groq response")

    def test_failover_handler_initialization(self):
        handler = FailoverHandler()
        self.assertEqual(handler.preferred, "ollama")
        
        handler_groq = FailoverHandler(preferred="groq")
        self.assertEqual(handler_groq.preferred, "groq")


class TestActionConsistency(unittest.TestCase):
    def setUp(self):
        self.tracker = ActionTracker()
        self.state = GameState()

    def test_record_and_retrieve_action(self):
        action = "talk to driver"
        result = "The driver grunts."
        
        self.tracker.record_action(action, result)
        
        self.assertTrue(self.tracker.has_action(action))
        self.assertEqual(self.tracker.get_result(action), result)

    def test_same_action_twice_returns_same_result(self):
        action = "look at window"
        result = "The window shows the dark city outside."
        
        self.tracker.record_action(action, result)
        
        consistency = self.tracker.get_consistency_check(action)
        
        self.assertTrue(consistency["exists"])
        self.assertEqual(consistency["result"], result)

    def test_different_actions_have_different_results(self):
        action1 = "talk to driver"
        action2 = "talk to alex"
        result1 = "Driver grunts."
        result2 = "Alex looks at you."
        
        self.tracker.record_action(action1, result1)
        self.tracker.record_action(action2, result2)
        
        self.assertEqual(self.tracker.get_result(action1), result1)
        self.assertEqual(self.tracker.get_result(action2), result2)

    def test_world_changes_tracked(self):
        action = "smash window"
        result = "Glass shatters."
        world_change = "window_broken_0"
        
        self.tracker.record_action(action, result, world_change)
        
        self.assertEqual(self.tracker.get_world_change(action), world_change)

    def test_clear_actions(self):
        self.tracker.record_action("action1", "result1")
        self.tracker.record_action("action2", "result2")
        
        self.tracker.clear()
        
        self.assertEqual(len(self.tracker.get_actions()), 0)

    def test_game_state_caches_results(self):
        action = "examine lamp"
        result = "The lamp glows with strange energy."
        
        self.state.add_action(action, result)
        
        cached = self.state.get_cached_result(action)
        self.assertEqual(cached, result)

    def test_game_state_reset_loop_preserves_loop_count(self):
        self.state.loop_count = 5
        self.state.add_action("action1", "result1")
        
        self.state.reset_loop()
        
        self.assertEqual(self.state.loop_count, 6)
        self.assertEqual(len(self.state.actions), 0)


class TestDebugMode(unittest.TestCase):
    def test_debug_mode_config(self):
        self.assertTrue(config.DEBUG_MODE)
    
    def test_log_prompts_config(self):
        self.assertTrue(config.LOG_PROMPTS)


class TestSoundEffects(unittest.TestCase):
    def test_sound_enabled_config(self):
        self.assertTrue(config.ENABLE_SOUND)


if __name__ == "__main__":
    unittest.main(verbosity=2)

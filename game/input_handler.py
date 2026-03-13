import pygame
import config
from llm import ollama, groq
from game.lore_loader import get_lore_loader


class InputHandler:
    def __init__(self, screen):
        self.screen = screen
        self.input_text = ""
        self.response_text = ""
        self.is_processing = False
        self.lore_loader = get_lore_loader()
        self.font = pygame.font.Font(None, 16)
        self.input_rect = pygame.Rect(10, 200, 240, 20)
        self.active = True

    def handle_event(self, event, game_state, loop_manager):
        if not self.active or game_state.game_over:
            return False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
            elif event.key == pygame.K_RETURN:
                if self.input_text.strip():
                    self._process_input(game_state, loop_manager)
                    return True
            else:
                if len(self.input_text) < 50:
                    self.input_text += event.unicode
        return False

    def _process_input(self, game_state, loop_manager):
        action_text = self.input_text.strip()
        self.input_text = ""
        self.is_processing = True

        try:
            prompt = self._build_prompt(action_text, game_state)
            response = self._send_to_llm(prompt)
            self.response_text = response

            game_state.add_action(action_text, response)

            should_reset = loop_manager.check_and_trigger_loop_reset(game_state)
            if not should_reset:
                game_state.advance_time()

            self._check_for_endings(action_text, response, game_state)

        except Exception as e:
            self.response_text = f"Error: {str(e)}"
        finally:
            self.is_processing = False

    def _build_prompt(self, action_text, game_state):
        setting = self.lore_loader.load_setting()
        npcs = self.lore_loader.load_npcs()
        endings = self.lore_loader.load_endings()

        npc_descriptions = []
        for npc_id, npc in npcs.items():
            desc = f"- {npc['name'].upper()}: {npc['description']}"
            npc_descriptions.append(desc)

        prompt = f"""You are the game master for "{setting['title']}", an 8-bit text adventure game.

SETTING: {setting['time_of_day']}. {setting['bus_description']}
The driver is silent. Other passengers are on the bus.

ATMOSPHERE: {setting['atmosphere']}
{setting['lamp_description']}

NPCS:
{chr(10).join(npc_descriptions)}

RULES:
{chr(10).join(f"- {rule}" for rule in setting['rules'])}

ENDINGS (only trigger if player explicitly performs these actions):
{chr(10).join(f"- {endings[e_id]['trigger']}: {endings[e_id]['name']}" for e_id in endings)}

CURRENT STATE:
- Loop: #{game_state.loop_count}, Minute: {game_state.current_minute}
- Actions taken: {game_state.actions if game_state.actions else "None yet"}
- World changes: {game_state.world_changes if game_state.world_changes else "None yet"}

The player performs this action: "{action_text}"

Respond with a descriptive, atmospheric response (2-4 sentences) that follows the game rules.
"""
        return prompt

    def _send_to_llm(self, prompt):
        if config.PREFERRED_LLM == "groq":
            if groq.is_available():
                return groq.generate(prompt)
            elif ollama.is_available():
                return ollama.generate(prompt)
        else:
            if ollama.is_available():
                return ollama.generate(prompt)
            elif groq.is_available():
                return groq.generate(prompt)

        raise RuntimeError("No LLM available")

    def _check_for_endings(self, action_text, response, game_state):
        endings = self.lore_loader.load_endings()
        action_lower = action_text.lower()

        for ending_id, ending in endings.items():
            trigger = ending.get("trigger", "").lower()
            if trigger in action_lower:
                game_state.set_ending(ending)
                self.response_text = ending.get("result", response)
                break

    def render(self, game_state):
        pygame.draw.rect(self.screen, config.UI_BG_COLOR, self.input_rect)
        pygame.draw.rect(self.screen, config.UI_TEXT_COLOR, self.input_rect, 1)

        if self.is_processing:
            input_surface = self.font.render("Processing...", True, config.UI_TEXT_COLOR)
        else:
            input_surface = self.font.render(self.input_text + "_", True, config.UI_TEXT_COLOR)
        self.screen.blit(input_surface, (self.input_rect.x + 5, self.input_rect.y + 2))

        if self.response_text:
            self._render_response_box()

    def _render_response_box(self):
        box_rect = pygame.Rect(10, 60, 300, 80)
        pygame.draw.rect(self.screen, config.BUS_WALL_COLOR, box_rect)
        pygame.draw.rect(self.screen, config.UI_TEXT_COLOR, box_rect, 1)

        words = self.response_text.split()
        lines = []
        current_line = []
        for word in words:
            test_line = " ".join(current_line + [word])
            if self.font.size(test_line)[0] < 280:
                current_line.append(word)
            else:
                lines.append(" ".join(current_line))
                current_line = [word]
        if current_line:
            lines.append(" ".join(current_line))

        for i, line in enumerate(lines[:4]):
            if i < 4:
                text_surface = self.font.render(line, True, config.UI_TEXT_COLOR)
                self.screen.blit(text_surface, (15, 65 + i * 18))

    def clear_response(self):
        self.response_text = ""

    def set_active(self, active):
        self.active = active

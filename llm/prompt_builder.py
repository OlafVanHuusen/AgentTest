from game.lore_loader import get_lore_loader


class PromptBuilder:
    def __init__(self, lore_loader=None):
        self.lore_loader = lore_loader or get_lore_loader()
        self.world_changes = []

    def add_world_change(self, change: str):
        if change not in self.world_changes:
            self.world_changes.append(change)

    def clear_world_changes(self):
        self.world_changes = []

    def build_system_prompt(self, game_state) -> str:
        setting = self.lore_loader.load_setting()
        npcs = self.lore_loader.load_npcs()

        prompt_parts = []

        prompt_parts.append(f'You are the game master for "{setting["title"]}", an 8-bit adventure game.')

        prompt_parts.append(f"\nSETTING: {setting['time_of_day']}. {setting['bus_description']}")
        prompt_parts.append("The player just woke up. The driver is silent.")
        prompt_parts.append("Other passengers are sleeping or on phones.")

        prompt_parts.append(f"\nATMOSPHERE: {setting['atmosphere']}")

        prompt_parts.append("\nNPCS:")
        for npc_id, npc_data in npcs.items():
            prompt_parts.append(f"- {npc_data['name'].upper()}: {npc_data['description']}")

        prompt_parts.append("\nRULES:")
        for rule in setting.get('rules', []):
            prompt_parts.append(f"- {rule}")

        if setting.get('lamp_description'):
            prompt_parts.append(f"\n{setting['lamp_description']}")

        prompt_parts.append(f"\nCURRENT STATE:")
        prompt_parts.append(f"- Loop: #{game_state.loop_count}, Minute: {game_state.current_minute}")

        if game_state.actions:
            prompt_parts.append(f"- Actions taken: {game_state.actions}")
        else:
            prompt_parts.append("- Actions taken: None yet")

        if self.world_changes:
            prompt_parts.append(f"- World changes: {', '.join(self.world_changes)}")
        else:
            prompt_parts.append("- World changes: None yet")

        prompt_parts.append("\nWhat happens when the player types an action?")

        return "\n".join(prompt_parts)

    def build_game_prompt(self, game_state, player_action: str) -> str:
        system_prompt = self.build_system_prompt(game_state)

        prompt = f"{system_prompt}\n\nPlayer action: {player_action}\n\nRespond with what happens next."
        return prompt


_prompt_builder = None


def get_prompt_builder() -> PromptBuilder:
    global _prompt_builder
    if _prompt_builder is None:
        _prompt_builder = PromptBuilder()
    return _prompt_builder


def build_system_prompt(game_state) -> str:
    return get_prompt_builder().build_system_prompt(game_state)


def build_game_prompt(game_state, player_action: str) -> str:
    return get_prompt_builder().build_game_prompt(game_state, player_action)

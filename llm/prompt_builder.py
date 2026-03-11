from game.lore_loader import get_lore_loader


class PromptBuilder:
    def __init__(self):
        self.lore_loader = get_lore_loader()
        self._system_prompt = None

    def get_system_prompt(self) -> str:
        if self._system_prompt is None:
            setting = self.lore_loader.load_setting()
            npcs = self.lore_loader.load_npcs()
            
            npc_descriptions = []
            for npc_id, npc_data in npcs.items():
                npc_descriptions.append(f"- {npc_data.get('name', npc_id)}: {npc_data.get('description', '')}")
            
            self._system_prompt = f"""You are the narrator of a text adventure game set on a Greyhound bus at {setting.get('time_of_day', '2:00 AM')}.
The atmosphere is: {setting.get('atmosphere', 'eerie silence')}
The bus is: {setting.get('bus_description', 'about 20 seats')}
The strange lamp: {setting.get('lamp_description', 'flickering brass lamp')}

NPCs on the bus:
{chr(10).join(npc_descriptions) if npc_descriptions else "- Silent driver at the front"}

Game Rules:
{chr(10).join(f"- {rule}" for rule in setting.get('rules', []))}

You respond to player actions in character. Be descriptive but concise. Consider the eerie atmosphere.
The driver never speaks but occasionally glances in the mirror."""
        
        return self._system_prompt

    def build_action_prompt(self, action: str, game_state) -> str:
        system = self.get_system_prompt()
        
        history = ""
        if game_state.actions:
            history = "Previous actions and results:\n"
            for i, (act, result) in enumerate(zip(game_state.actions, game_state.action_results.values()), 1):
                history += f"{i}. {act}: {result}\n"
        
        return f"""{system}

{history}
The player does: {action}

Narrator response:"""

    def build_first_action_prompt(self, action: str) -> str:
        system = self.get_system_prompt()
        
        return f"""{system}

The player boards the bus at 2 AM and does: {action}

Narrator response:"""

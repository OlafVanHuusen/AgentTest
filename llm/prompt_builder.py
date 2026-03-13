import json
from typing import Optional
from game.state import GameState


class PromptBuilder:
    def __init__(self, lore_loader):
        self.lore_loader = lore_loader

    def build_system_prompt(self) -> str:
        setting = self.lore_loader.get_setting()
        npcs = self.lore_loader.npcs.get("npcs", [])

        prompt_parts = [
            f"# {setting.get('title', 'Timeloop Bus')}",
            f"Time: {setting.get('time_of_day', '2:00 AM')}",
            f"Atmosphere: {setting.get('atmosphere', '')}",
            f"Setting: {setting.get('bus_description', '')}",
            "",
            "## Rules"
        ]

        for rule in setting.get("rules", []):
            prompt_parts.append(f"- {rule}")

        prompt_parts.extend([
            "",
            "## Characters"
        ])

        for npc in npcs:
            prompt_parts.extend([
                f"### {npc.get('name', 'Unknown')}",
                f"Description: {npc.get('description', '')}",
                f"Attributes: {', '.join(npc.get('attributes', []))}",
                f"Location: {npc.get('location', '')}",
                ""
            ])

        prompt_parts.extend([
            "You are the game master. Describe what happens concisely (1-3 sentences).",
            "If the player tries to interact with a character, include their response.",
            "Track any world changes that persist until reset."
        ])

        return "\n".join(prompt_parts)

    def build_game_prompt(self, state: GameState, player_action: str) -> str:
        system = self.build_system_prompt()

        prompt_parts = [
            system,
            "",
            f"## Current State",
            f"Loop: {state.loop_count}",
            f"Time: {state.current_minute}:00",
            f"Actions this loop: {state.actions_this_loop}",
            ""
        ]

        if state.world_changes:
            prompt_parts.append("## World Changes (this loop)")
            for action, change in state.world_changes.items():
                prompt_parts.append(f"- {action}: {change}")
            prompt_parts.append("")

        prompt_parts.extend([
            f"## Player Action",
            f"{player_action}",
            "",
            "## Response"
        ])

        return "\n".join(prompt_parts)
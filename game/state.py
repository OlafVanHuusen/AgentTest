"""Game state management for Timeloop Bus."""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class GameState:
    """Manages the current state of the game."""

    loop_count: int = 1
    current_minute: int = 0
    action_history: list[str] = field(default_factory=list)
    current_dialogue: str = ""
    player_input: str = ""
    game_over: bool = False
    ending_triggered: Optional[str] = None

    def __post_init__(self):
        if self.current_minute == 0:
            self.current_minute = 2

    def advance_time(self) -> None:
        """Advance the game time by one minute."""
        self.current_minute += 1

    def add_action(self, action: str) -> None:
        """Add an action to the history."""
        self.action_history.append(action)

    def set_dialogue(self, dialogue: str) -> None:
        """Set the current dialogue to display."""
        self.current_dialogue = dialogue

    def reset_loop(self) -> None:
        """Reset the current loop but keep player memory."""
        self.current_minute = 2
        self.action_history.clear()
        self.current_dialogue = ""
        self.player_input = ""
        self.game_over = False
        self.ending_triggered = None
        self.loop_count += 1

    def should_reset(self) -> bool:
        """Check if it's time to reset the loop."""
        return self.current_minute >= 2 + 10

    def get_time_string(self) -> str:
        """Get the current time as a formatted string."""
        hour = self.current_minute // 60
        minute = self.current_minute % 60
        return f"{hour:02d}:{minute:02d}"

    def trigger_ending(self, ending_id: str) -> None:
        """Trigger a game ending."""
        self.game_over = True
        self.ending_triggered = ending_id

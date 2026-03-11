from game.state import GameState


def advance_minute(game_state: GameState) -> bool:
    return game_state.advance_time()


def get_formatted_time(game_state: GameState) -> str:
    hour = 2
    minute = game_state.current_minute
    return f"{hour:02d}:{minute:02d}"

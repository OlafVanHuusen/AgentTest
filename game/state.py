class GameState:
    def __init__(self):
        self.loop_count: int = 1
        self.current_minute: int = 0
        self.actions_taken: list[str] = []
        self.world_changes: dict = {}
        self.ending_triggered: bool = False
        self.game_over: bool = False
        self.ending: str | None = None
        self.actions_this_loop: int = 0
        self.max_actions_per_loop: int = 10
        self.action_results: dict = {}

    def advance_time(self):
        self.current_minute += 1
        self.actions_this_loop += 1
        if self.current_minute >= self.get_max_minute():
            return True
        if self.actions_this_loop >= self.max_actions_per_loop:
            return True
        return False

    def get_max_minute(self):
        return 12

    def add_action(self, action_text, result):
        self.actions_taken.append(action_text)
        self.action_results[hash(action_text)] = result

    def get_cached_result(self, action_text):
        return self.action_results.get(hash(action_text))

    def reset_loop(self):
        self.current_minute = 0
        self.actions_this_loop = 0
        self.actions_taken = []
        self.action_results = {}
        self.world_changes = {}
        self.loop_count += 1

    def set_ending(self, ending):
        self.ending = ending
        self.ending_triggered = True
        self.game_over = True

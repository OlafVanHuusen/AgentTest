class ActionTracker:
    def __init__(self):
        self._action_results = {}

    def _get_hash(self, action_text):
        return hash(action_text.lower().strip())

    def get_result(self, action_text):
        action_hash = self._get_hash(action_text)
        return self._action_results.get(action_hash)

    def store_result(self, action_text, result):
        action_hash = self._get_hash(action_text)
        self._action_results[action_hash] = result

    def has_result(self, action_text):
        action_hash = self._get_hash(action_text)
        return action_hash in self._action_results

    def clear(self):
        self._action_results = {}

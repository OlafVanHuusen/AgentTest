from typing import Dict, List, Any


class ActionTracker:
    def __init__(self):
        self._actions: List[str] = []
        self._results: Dict[str, Any] = {}
        self._world_changes: Dict[str, Any] = {}

    def record_action(self, action: str, result: str, world_change: str = None):
        self._actions.append(action)
        self._results[action] = result
        if world_change:
            self._world_changes[action] = world_change

    def get_actions(self) -> List[str]:
        return self._actions.copy()

    def get_result(self, action: str) -> str:
        return self._results.get(action)

    def get_world_change(self, action: str) -> str:
        return self._world_changes.get(action)

    def has_action(self, action: str) -> bool:
        return action in self._results

    def get_consistency_check(self, action: str) -> Dict[str, Any]:
        return {
            "action": action,
            "result": self.get_result(action),
            "world_change": self.get_world_change(action),
            "exists": self.has_action(action)
        }

    def clear(self):
        self._actions.clear()
        self._results.clear()
        self._world_changes.clear()
import re
from game.lore_loader import get_lore_loader


class EndingDetector:
    ENDING_TRIGGERS = {
        "ending_1_coma": [
            r"\blook\s+(at\s+)?(the\s+)?lamp\b",
            r"\bexamine\s+(the\s+)?lamp\b",
            r"\binspect\s+(the\s+)?lamp\b",
            r"\blook\s+at\s+(the\s+)?driver'?s?\s+lamp\b",
        ],
        "ending_2_dark_city": [
            r"\bsmash\s+(the\s+)?lamp\b",
            r"\bbreak\s+(the\s+)?lamp\b",
            r"\bdestroy\s+(the\s+)?lamp\b",
            r"\bshatter\s+(the\s+)?lamp\b",
        ],
        "ending_3_give_up": [
            r"\bkill\s+(myself|me)\b",
            r"\bend\s+it\b",
            r"\bhow\s+to\s+die\b",
            r"\bsuicide\b",
            r"\bend\s+(the\s+)?loop\b",
        ],
    }

    def __init__(self):
        self.lore_loader = get_lore_loader()
        self._compile_patterns()

    def _compile_patterns(self):
        self.compiled_patterns = {}
        for ending_id, patterns in self.ENDING_TRIGGERS.items():
            self.compiled_patterns[ending_id] = [
                re.compile(p, re.IGNORECASE) for p in patterns
            ]

    def check_input(self, player_input: str) -> str | None:
        if not player_input:
            return None

        for ending_id, patterns in self.compiled_patterns.items():
            for pattern in patterns:
                if pattern.search(player_input):
                    return ending_id
        return None

    def get_ending_text(self, ending_id: str) -> str | None:
        ending = self.lore_loader.get_ending(ending_id)
        if ending:
            return ending.get("result", "")
        return None

    def get_ending_name(self, ending_id: str) -> str | None:
        ending = self.lore_loader.get_ending(ending_id)
        if ending:
            return ending.get("name", "")
        return None


_ending_detector = None


def get_ending_detector() -> EndingDetector:
    global _ending_detector
    if _ending_detector is None:
        _ending_detector = EndingDetector()
    return _ending_detector

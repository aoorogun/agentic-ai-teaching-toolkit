from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Optional

_BLOCKED_CATEGORIES: Dict[str, List[str]] = {
    "weapons_or_explosives": ["build a bomb", "make explosives", "weapon schematic"],
    "malware": ["write malware", "write a virus", "ransomware code"],
    "self_harm": ["kill myself", "self harm", "suicide method"],
    "personal_data_exfiltration": ["steal personal data", "dox someone", "leak private records"],
}


@dataclass
class SafetyDecision:
    allowed: bool
    category: Optional[str] = None
    reason: Optional[str] = None


class SafetyFilter:
    def __init__(self, extra_blocklist: Optional[Dict[str, List[str]]] = None) -> None:
        self._blocklist = dict(_BLOCKED_CATEGORIES)
        if extra_blocklist:
            self._blocklist.update(extra_blocklist)

    def evaluate(self, text: str) -> SafetyDecision:
        lowered = text.lower()
        for category, phrases in self._blocklist.items():
            for phrase in phrases:
                if phrase in lowered:
                    return SafetyDecision(allowed=False, category=category, reason=phrase)
        return SafetyDecision(allowed=True)

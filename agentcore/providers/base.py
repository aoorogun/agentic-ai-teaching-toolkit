from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class ProviderDecision:
    kind: str
    content: Optional[str] = None
    tool_name: Optional[str] = None
    tool_arguments: Optional[Dict[str, Any]] = None


class Provider:
    def decide(self, history: List[Dict[str, Any]], tool_specs: List[Dict[str, Any]]) -> ProviderDecision:
        raise NotImplementedError

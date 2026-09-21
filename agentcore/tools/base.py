from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class ToolResult:
    success: bool
    output: Any
    error: str = ""


class Tool:
    name: str = ""
    description: str = ""
    parameters: Dict[str, Any] = {}

    def run(self, **kwargs: Any) -> ToolResult:
        raise NotImplementedError

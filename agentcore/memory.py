from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class ConversationMemory:
    history: List[Dict[str, Any]] = field(default_factory=list)

    def add_user_message(self, content: str) -> None:
        self.history.append({"role": "user", "content": content})

    def add_assistant_message(self, content: str) -> None:
        self.history.append({"role": "assistant", "content": content})

    def add_tool_call(self, name: str, arguments: Dict[str, Any]) -> None:
        self.history.append({"role": "tool_call", "name": name, "arguments": arguments})

    def add_tool_result(self, name: str, result: Any) -> None:
        self.history.append({"role": "tool_result", "name": name, "result": result})

    def get_history(self) -> List[Dict[str, Any]]:
        return list(self.history)

    def clear(self) -> None:
        self.history = []

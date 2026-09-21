from __future__ import annotations
from typing import Dict, List
from agentcore.tools.base import Tool, ToolResult


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: Dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        self._tools[tool.name] = tool

    def get(self, name: str) -> Tool:
        if name not in self._tools:
            raise KeyError(name)
        return self._tools[name]

    def has(self, name: str) -> bool:
        return name in self._tools

    def list_specs(self) -> List[Dict]:
        return [
            {"name": tool.name, "description": tool.description, "parameters": tool.parameters}
            for tool in self._tools.values()
        ]

    def dispatch(self, name: str, arguments: Dict) -> ToolResult:
        tool = self.get(name)
        return tool.run(**arguments)

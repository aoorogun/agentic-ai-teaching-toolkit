from __future__ import annotations
import difflib
import json
import os
from typing import Any, Dict

from agentcore.tools.base import Tool, ToolResult

_DATA_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "data",
    "knowledge_base.json",
)


def _load_terms() -> Dict[str, str]:
    with open(_DATA_PATH, "r", encoding="utf-8") as handle:
        return json.load(handle)


class KnowledgeBaseTool(Tool):
    name = "knowledge_base"
    description = "Looks up definitions of computing and AI terms from a curated glossary."
    parameters = {
        "type": "object",
        "properties": {
            "term": {"type": "string"}
        },
        "required": ["term"],
    }

    def __init__(self) -> None:
        self._terms = _load_terms()

    def run(self, **kwargs: Any) -> ToolResult:
        term = str(kwargs.get("term", "")).strip().lower()
        if term in self._terms:
            return ToolResult(success=True, output=self._terms[term])
        matches = difflib.get_close_matches(term, self._terms.keys(), n=1, cutoff=0.6)
        if matches:
            return ToolResult(success=True, output=self._terms[matches[0]])
        return ToolResult(success=False, output=None, error="term_not_found")

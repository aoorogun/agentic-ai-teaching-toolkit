from __future__ import annotations
import re
from typing import Any, Dict, List, Optional

from agentcore.providers.base import Provider, ProviderDecision

_CONVERT_PATTERN = re.compile(
    r"convert\s+(-?\d+(?:\.\d+)?)\s*([a-zA-Z]+)\s+to\s+([a-zA-Z]+)", re.IGNORECASE
)
_MATH_PATTERN = re.compile(r"^[\d\s+\-*/().%]+$")


def _latest_user_index(history: List[Dict[str, Any]]) -> int:
    for index in range(len(history) - 1, -1, -1):
        if history[index]["role"] == "user":
            return index
    return -1


def _tool_result_after(history: List[Dict[str, Any]], start_index: int) -> Optional[Dict[str, Any]]:
    for entry in history[start_index + 1:]:
        if entry["role"] == "tool_result":
            return entry
    return None


class RuleBasedProvider(Provider):
    def decide(self, history: List[Dict[str, Any]], tool_specs: List[Dict[str, Any]]) -> ProviderDecision:
        user_index = _latest_user_index(history)
        if user_index == -1:
            return ProviderDecision(kind="final", content="No input provided.")
        user_text = history[user_index]["content"].strip()
        existing_result = _tool_result_after(history, user_index)
        if existing_result is not None:
            return ProviderDecision(kind="final", content=str(existing_result["result"]))
        convert_match = _CONVERT_PATTERN.search(user_text)
        if convert_match:
            value, from_unit, to_unit = convert_match.groups()
            return ProviderDecision(
                kind="tool_call",
                tool_name="unit_converter",
                tool_arguments={"value": float(value), "from_unit": from_unit, "to_unit": to_unit},
            )
        if user_text.lower().startswith("summarize:"):
            passage = user_text.split(":", 1)[1].strip()
            return ProviderDecision(
                kind="tool_call",
                tool_name="summarizer",
                tool_arguments={"text": passage, "max_sentences": 2},
            )
        lowered = user_text.lower()
        if lowered.startswith("define ") or lowered.startswith("what is "):
            term = lowered.replace("define", "").replace("what is", "").strip(" ?")
            return ProviderDecision(
                kind="tool_call",
                tool_name="knowledge_base",
                tool_arguments={"term": term},
            )
        stripped_math = user_text.replace(" ", "")
        if _MATH_PATTERN.match(stripped_math) and any(ch.isdigit() for ch in stripped_math):
            return ProviderDecision(
                kind="tool_call",
                tool_name="calculator",
                tool_arguments={"expression": user_text},
            )
        return ProviderDecision(
            kind="final",
            content="I can help with calculations, unit conversions, glossary lookups (define X) and summaries (summarize: text).",
        )

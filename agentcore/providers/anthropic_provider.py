from __future__ import annotations
import json
import os
from typing import Any, Dict, List

from agentcore.providers.base import Provider, ProviderDecision


class AnthropicProvider(Provider):
    def __init__(self, model_name: str = "claude-sonnet-4-6") -> None:
        try:
            import anthropic
        except ImportError as exc:
            raise RuntimeError("anthropic_package_not_installed") from exc
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise RuntimeError("anthropic_api_key_missing")
        self._client = anthropic.Anthropic(api_key=api_key)
        self._model_name = model_name

    def _build_messages(self, history: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        messages: List[Dict[str, Any]] = []
        for entry in history:
            if entry["role"] == "user":
                messages.append({"role": "user", "content": entry["content"]})
            elif entry["role"] == "assistant":
                messages.append({"role": "assistant", "content": entry["content"]})
            elif entry["role"] == "tool_result":
                messages.append({
                    "role": "user",
                    "content": f"Tool {entry['name']} returned: {json.dumps(entry['result'])}",
                })
        return messages

    def _build_tools(self, tool_specs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        tools = []
        for spec in tool_specs:
            tools.append({
                "name": spec["name"],
                "description": spec["description"],
                "input_schema": spec["parameters"],
            })
        return tools

    def decide(self, history: List[Dict[str, Any]], tool_specs: List[Dict[str, Any]]) -> ProviderDecision:
        messages = self._build_messages(history)
        tools = self._build_tools(tool_specs)
        response = self._client.messages.create(
            model=self._model_name,
            max_tokens=1024,
            messages=messages,
            tools=tools,
        )
        for block in response.content:
            if block.type == "tool_use":
                return ProviderDecision(
                    kind="tool_call",
                    tool_name=block.name,
                    tool_arguments=dict(block.input),
                )
        text_blocks = [block.text for block in response.content if block.type == "text"]
        return ProviderDecision(kind="final", content="\n".join(text_blocks))

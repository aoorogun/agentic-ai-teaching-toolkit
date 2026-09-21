from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List

from agentcore.config import AgentConfig
from agentcore.logging_utils import build_logger, log_event
from agentcore.memory import ConversationMemory
from agentcore.providers.base import Provider
from agentcore.registry import ToolRegistry
from agentcore.safety import SafetyFilter


@dataclass
class AgentResult:
    final_text: str
    transcript: List[Dict[str, Any]] = field(default_factory=list)


class Agent:
    def __init__(
        self,
        config: AgentConfig,
        provider: Provider,
        registry: ToolRegistry,
        memory: ConversationMemory,
        safety: SafetyFilter,
    ) -> None:
        self._config = config
        self._provider = provider
        self._registry = registry
        self._memory = memory
        self._safety = safety
        self._logger = build_logger("agent")

    def run(self, user_input: str) -> AgentResult:
        decision = self._safety.evaluate(user_input)
        if not decision.allowed:
            refusal = f"Request declined. Category: {decision.category}."
            log_event(self._logger, "refusal", {"category": decision.category, "reason": decision.reason})
            return AgentResult(final_text=refusal, transcript=self._memory.get_history())
        self._memory.add_user_message(user_input)
        for _ in range(self._config.max_iterations):
            provider_decision = self._provider.decide(self._memory.get_history(), self._registry.list_specs())
            if provider_decision.kind == "tool_call":
                arguments = provider_decision.tool_arguments or {}
                self._memory.add_tool_call(provider_decision.tool_name, arguments)
                log_event(self._logger, "tool_call", {"name": provider_decision.tool_name, "arguments": arguments})
                result = self._registry.dispatch(provider_decision.tool_name, arguments)
                output = result.output if result.success else f"error: {result.error}"
                self._memory.add_tool_result(provider_decision.tool_name, output)
                log_event(self._logger, "tool_result", {"name": provider_decision.tool_name, "output": output})
                continue
            final_text = provider_decision.content or ""
            self._memory.add_assistant_message(final_text)
            return AgentResult(final_text=final_text, transcript=self._memory.get_history())
        return AgentResult(
            final_text="Maximum iterations reached without a final answer.",
            transcript=self._memory.get_history(),
        )

from __future__ import annotations
from dataclasses import dataclass


@dataclass
class AgentConfig:
    provider_name: str = "rule_based"
    model_name: str = "claude-sonnet-4-6"
    max_iterations: int = 5
    temperature: float = 0.0

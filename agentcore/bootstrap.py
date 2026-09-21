from __future__ import annotations
from agentcore.agent import Agent
from agentcore.config import AgentConfig
from agentcore.memory import ConversationMemory
from agentcore.orchestrator import TaskOrchestrator
from agentcore.providers.rule_based import RuleBasedProvider
from agentcore.registry import ToolRegistry
from agentcore.safety import SafetyFilter
from agentcore.tools.calculator import CalculatorTool
from agentcore.tools.knowledge_base import KnowledgeBaseTool
from agentcore.tools.summarizer import TextSummarizerTool
from agentcore.tools.unit_converter import UnitConverterTool


def build_default_registry() -> ToolRegistry:
    registry = ToolRegistry()
    registry.register(CalculatorTool())
    registry.register(UnitConverterTool())
    registry.register(KnowledgeBaseTool())
    registry.register(TextSummarizerTool())
    return registry


def build_agent(provider_name: str = "rule_based", model_name: str = "claude-sonnet-4-6") -> Agent:
    config = AgentConfig(provider_name=provider_name, model_name=model_name)
    registry = build_default_registry()
    memory = ConversationMemory()
    safety = SafetyFilter()
    if provider_name == "anthropic":
        from agentcore.providers.anthropic_provider import AnthropicProvider
        provider = AnthropicProvider(model_name=model_name)
    else:
        provider = RuleBasedProvider()
    return Agent(config=config, provider=provider, registry=registry, memory=memory, safety=safety)


def build_orchestrator(provider_name: str = "rule_based", model_name: str = "claude-sonnet-4-6") -> TaskOrchestrator:
    agent = build_agent(provider_name=provider_name, model_name=model_name)
    return TaskOrchestrator(agent)

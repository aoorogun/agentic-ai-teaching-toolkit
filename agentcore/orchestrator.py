from __future__ import annotations
import re
from dataclasses import dataclass, field
from typing import List

from agentcore.agent import Agent, AgentResult
from agentcore.tools.summarizer import TextSummarizerTool

_SPLIT_PATTERN = re.compile(r"\s*(?:;|\bthen\b)\s*", re.IGNORECASE)


@dataclass
class OrchestratorResult:
    subtask_results: List[AgentResult] = field(default_factory=list)
    combined_summary: str = ""


class TaskOrchestrator:
    def __init__(self, agent: Agent) -> None:
        self._agent = agent
        self._summarizer = TextSummarizerTool()

    def decompose(self, task: str) -> List[str]:
        parts = [p.strip() for p in _SPLIT_PATTERN.split(task) if p.strip()]
        return parts if parts else [task.strip()]

    def run(self, task: str) -> OrchestratorResult:
        subtasks = self.decompose(task)
        results = [self._agent.run(subtask) for subtask in subtasks]
        combined_text = " ".join(
            f"{subtask}: {result.final_text}." for subtask, result in zip(subtasks, results)
        )
        summary_result = self._summarizer.run(text=combined_text, max_sentences=len(subtasks))
        summary = summary_result.output if summary_result.success else combined_text
        return OrchestratorResult(subtask_results=results, combined_summary=summary)

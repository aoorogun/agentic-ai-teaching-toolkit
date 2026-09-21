from __future__ import annotations
import re
from collections import Counter
from typing import Any, List

from agentcore.tools.base import Tool, ToolResult

_STOPWORDS = {
    "the", "a", "an", "and", "or", "but", "is", "are", "was", "were", "in", "on",
    "at", "to", "for", "of", "with", "by", "this", "that", "it", "as", "be",
    "has", "have", "had", "from", "which", "will", "can", "not",
}


def _split_sentences(text: str) -> List[str]:
    candidates = re.split(r"(?<=[.!?])\s+", text.strip())
    return [c for c in candidates if c]


def _score_sentences(sentences: List[str]) -> List[float]:
    word_counts: Counter = Counter()
    tokenized: List[List[str]] = []
    for sentence in sentences:
        words = [w.lower() for w in re.findall(r"[A-Za-z']+", sentence) if w.lower() not in _STOPWORDS]
        tokenized.append(words)
        word_counts.update(words)
    scores = []
    for words in tokenized:
        if not words:
            scores.append(0.0)
            continue
        scores.append(sum(word_counts[w] for w in words) / len(words))
    return scores


class TextSummarizerTool(Tool):
    name = "summarizer"
    description = "Produces an extractive summary of a passage by selecting the highest scoring sentences."
    parameters = {
        "type": "object",
        "properties": {
            "text": {"type": "string"},
            "max_sentences": {"type": "integer"},
        },
        "required": ["text"],
    }

    def run(self, **kwargs: Any) -> ToolResult:
        text = kwargs.get("text", "")
        max_sentences = int(kwargs.get("max_sentences", 3))
        sentences = _split_sentences(text)
        if not sentences:
            return ToolResult(success=False, output=None, error="empty_text")
        scores = _score_sentences(sentences)
        ranked_indices = sorted(range(len(sentences)), key=lambda i: scores[i], reverse=True)
        selected_indices = sorted(ranked_indices[:max_sentences])
        summary = " ".join(sentences[i] for i in selected_indices)
        return ToolResult(success=True, output=summary)

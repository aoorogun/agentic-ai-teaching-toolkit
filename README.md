# Agentic AI Teaching Toolkit

A modular, testable reference implementation of a tool-using AI agent, built as
a teaching exemplar for a Computing curriculum covering software engineering,
artificial intelligence and responsible AI use. The project demonstrates the
core mechanics of agentic AI (planning, tool use, memory, orchestration and
safety guardrails) in plain, readable Python with no external dependencies
required to run the core demo.

## Why this project exists

It is designed to be used directly in teaching: as a worked example in
lectures, as a starting codebase for student coursework, and as a live
demonstration of how an AI agent decides when to call a tool, executes it,
and folds the result back into its reasoning. A rule-based provider means the
whole system runs offline and deterministically, which makes it suitable for
classroom demonstrations and automated marking without requiring API keys or
network access. An optional provider backed by the Anthropic API is included
for students who want to see the same architecture driven by a real language
model with function calling.

## Architecture

The system is split into independent, single-responsibility modules:

- `agentcore.tools` - a family of tools (calculator, unit converter, glossary
  lookup, extractive summarizer), each implementing a common `Tool` interface
  so new tools can be added without touching the agent loop.
- `agentcore.registry` - a `ToolRegistry` that holds available tools and
  exposes their schemas to a provider.
- `agentcore.providers` - pluggable decision-making backends. `RuleBasedProvider`
  is a deterministic, offline provider; `AnthropicProvider` calls the Anthropic
  Messages API with function calling for the same tool set.
- `agentcore.memory` - a simple conversation memory recording user turns, tool
  calls and tool results.
- `agentcore.safety` - a `SafetyFilter` implementing a basic, explicit
  keyword-based guardrail used to teach the concept of pre-execution content
  policy checks. It is intentionally simple and is documented as a teaching
  device rather than a production moderation system.
- `agentcore.agent` - the `Agent` class implementing the perceive-plan-act-observe
  loop up to a configurable number of iterations.
- `agentcore.orchestrator` - a `TaskOrchestrator` that splits a compound task
  into subtasks and runs the agent on each in turn, then produces a combined
  summary, illustrating multi-step agentic orchestration.

See `docs/architecture.md` for a full walkthrough suitable for lecture slides.

## Requirements

- Python 3.9 or later
- `pip install -r requirements.txt` for running tests
- `pip install -r requirements-llm.txt` only if you want to use the optional
  Anthropic-backed provider

## Running the demo

From the repository root, with no installation step required:

```
python examples/run_single_agent.py
python examples/run_orchestrator.py
```

Or via the command-line interface:

```
python -m agentcore.cli run "define agentic ai"
python -m agentcore.cli run "convert 5 km to m"
python -m agentcore.cli orchestrate "2 + 2; define retrieval augmented generation"
python -m agentcore.cli list-tools
```

To use the Anthropic-backed provider instead of the offline rule-based one,
set `ANTHROPIC_API_KEY` (see `.env.example`) and pass `--provider anthropic`.

## Running the tests

```
pip install -r requirements.txt
pytest
```

All tests run offline against the rule-based provider, so the suite is
suitable for automated coursework marking.

## Curriculum use

- `docs/architecture.md` - a module-by-module explanation suitable for a
  lecture or lab handout on agentic AI system design.
- `docs/assessment_rubric.md` - a marking rubric for a coursework assignment
  built around extending this toolkit with a new tool.
- `docs/student_exercises.md` - a progressive sequence of exercises, from
  adding a single tool through to extending the orchestrator and wiring in a
  real language model provider.

## Responsible AI note

The `SafetyFilter` in this repository is a simplified, transparent example
built for teaching the concept of input-side guardrails. It is not a
substitute for a production content moderation system and should be
presented to students as such.

## License

MIT

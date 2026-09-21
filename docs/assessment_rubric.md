# Assessment Rubric: Extend the Agentic AI Toolkit

Coursework brief: implement one new `Tool`, wire it into the rule-based
provider and the tool registry, write tests for it, and submit a short
written reflection on a responsible AI consideration raised by the tool.

Total: 100 marks, mapped to UK undergraduate degree classification bands.

| Criterion | Weighting | First (70-100) | 2:1 (60-69) | 2:2 (50-59) | Third / Fail (0-49) |
|---|---|---|---|---|---|
| Correctness of the tool | 25% | Tool handles all specified cases and edge cases correctly, with clear input validation. | Tool handles the main cases correctly; minor edge cases missed. | Tool works for typical inputs but has noticeable gaps. | Tool does not reliably produce correct output. |
| Software engineering quality | 20% | Follows the existing `Tool` interface exactly; clean, modular, single-responsibility code; no dead code. | Follows the interface with minor inconsistencies; mostly clean code. | Interface followed loosely; some duplication or unclear structure. | Interface not followed, or code is difficult to follow. |
| Integration with the agent | 20% | New routing logic in the provider is precise and does not regress existing routes; registry integration is correct. | Integration works; one minor issue with routing precision. | Integration works but is fragile or overly broad in what it matches. | Tool is not actually reachable through the agent. |
| Testing | 20% | Comprehensive tests covering success, failure and edge cases; tests pass and are deterministic. | Good coverage of success and failure cases; minor gaps. | Basic tests present but shallow coverage. | Little or no meaningful testing. |
| Responsible AI reflection | 15% | Sharp, specific discussion of a real risk or limitation introduced by the tool (for example, a guardrail gap, a data quality risk, or a misuse scenario) with a concrete mitigation. | Sound discussion of a relevant risk with a reasonable mitigation. | General or generic discussion of AI risk not clearly tied to the tool. | Reflection missing or not related to the tool built. |

## Submission checklist

- New file under `agentcore/tools/` implementing `Tool`.
- Registration of the new tool in `agentcore/bootstrap.py`.
- New routing branch in `agentcore/providers/rule_based.py`.
- New test file under `tests/` exercising the tool directly and, ideally, via
  `Agent.run`.
- A written reflection of 200 to 400 words.

## Suggested tools for cohort variation

Currency converter with a fixed illustrative exchange-rate table, a simple
readability scorer, a basic sentiment classifier using a small lexicon, or a
date and time calculator. Assigning different tools across a cohort reduces
the risk of collusion while keeping the assessment structurally identical for
fair, consistent marking.

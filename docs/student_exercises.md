# Student Exercises

A progressive sequence of exercises built on this toolkit, suitable for a
Software Engineering or AI module using agentic systems as a case study.

## Exercise 1: Add a tool

Implement a `CurrencyConverterTool` following the `Tool` interface used by
`CalculatorTool`. Use a small, fixed lookup table of exchange rates rather
than a live API, and clearly document that the rates are illustrative.

## Exercise 2: Test the tool

Write a `pytest` test module for the new tool covering at least one
successful conversion, one unsupported currency pair, and one invalid input
type.

## Exercise 3: Route natural language to the tool

Extend `RuleBasedProvider.decide` with a regular expression that recognises
instructions such as `"convert 50 usd to gbp"` and routes them to the new
tool with the correct arguments extracted.

## Exercise 4: Add a guardrail

Add a new category to `SafetyFilter` covering a risk relevant to your tool
(for example, a request to use the currency converter to help structure a
transaction to evade a reporting threshold). Write a test that confirms the
request is blocked, and one that confirms an unrelated request is not
affected.

## Exercise 5: Extend the orchestrator

Modify `TaskOrchestrator` so that if any subtask's agent result contains the
word `"error"`, the orchestrator stops running further subtasks and reports
which subtask failed, rather than silently continuing. Add a test that
exercises this new behaviour with a deliberately failing subtask.

## Stretch exercise: connect a real model

Set `ANTHROPIC_API_KEY` and run the CLI with `--provider anthropic` instead
of the default rule-based provider. Compare the tool-calling behaviour of the
language model against the deterministic rule-based provider on the same set
of five example queries, and write a short comparison of where the two
approaches agree and where they diverge.

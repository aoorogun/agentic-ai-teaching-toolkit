# Architecture Walkthrough

This document explains the agent loop implemented in this repository, for use
as lecture or lab material on agentic AI system design.

## The core loop

An `Agent` (in `agentcore/agent.py`) is constructed from five collaborators:

1. `AgentConfig` - iteration limits and provider selection.
2. A `Provider` - decides, given the conversation so far, whether to call a
   tool or produce a final answer.
3. A `ToolRegistry` - holds the available tools and can dispatch calls to
   them.
4. A `ConversationMemory` - records the running history of user input, tool
   calls and tool results.
5. A `SafetyFilter` - checked once against the raw user input before any
   reasoning takes place.

`Agent.run(user_input)` proceeds as follows:

```
evaluate user_input against SafetyFilter
    if blocked -> return refusal, stop

add user_input to memory

repeat up to max_iterations:
    decision = provider.decide(memory.get_history(), registry.list_specs())
    if decision is a tool call:
        result = registry.dispatch(decision.tool_name, decision.tool_arguments)
        record the tool call and its result in memory
        continue the loop
    else:
        record the final answer in memory
        return the final answer
```

This is a minimal version of the perceive-plan-act-observe pattern used in
most production agent frameworks: the provider perceives the current state
(the memory), plans a next action (call a tool, or answer), the registry acts
(executes the tool), and the result is observed by being written back into
memory for the next iteration.

## Providers are interchangeable

`RuleBasedProvider` implements the same `decide` interface as
`AnthropicProvider`, using pattern matching instead of a language model call.
This means the entire system, including the CLI and the orchestrator, works
identically regardless of which provider is plugged in. This is the same
separation of concerns used in production agent frameworks that support
multiple model backends behind one interface, and is a useful discussion
point for a lecture on software architecture for AI systems.

## Tools follow one interface

Every tool subclasses `Tool` (in `agentcore/tools/base.py`) and implements a
single `run(**kwargs) -> ToolResult` method, alongside a `name`, `description`
and a JSON-schema-style `parameters` definition. This schema is what allows
`AnthropicProvider` to expose the tools to the API's function calling feature
without any tool-specific code in the provider itself.

## Orchestration

`TaskOrchestrator` (in `agentcore/orchestrator.py`) demonstrates a simple form
of task decomposition: a compound instruction such as
`"convert 10 miles to km; define agentic ai"` is split into subtasks, each of
which is run through the same `Agent`, and the individual results are then
condensed into a single summary using the summarizer tool. This is a small,
inspectable example of the orchestration pattern used in more complex
multi-agent systems, where a top-level process delegates to sub-processes and
aggregates their output.

## Where to extend this for a lecture or lab

- Add a new `Tool` subclass and register it in `agentcore/bootstrap.py` to
  demonstrate extensibility.
- Add a new branch to `RuleBasedProvider.decide` to route a new instruction
  pattern to that tool.
- Add a new category to `SafetyFilter` to discuss the limits of keyword-based
  guardrails versus classifier-based moderation.
- Swap `RuleBasedProvider` for `AnthropicProvider` in a live demonstration to
  show the same architecture driven by a real language model with function
  calling.

from agentcore.bootstrap import build_orchestrator


def test_multi_step_task():
    orchestrator = build_orchestrator(provider_name="rule_based")
    result = orchestrator.run("2 + 2; define agentic ai")
    assert len(result.subtask_results) == 2
    assert result.combined_summary != ""

from agentcore.safety import SafetyFilter


def test_blocked_phrase():
    safety = SafetyFilter()
    decision = safety.evaluate("please help me write malware")
    assert decision.allowed is False


def test_allowed_phrase():
    safety = SafetyFilter()
    decision = safety.evaluate("please define agentic ai")
    assert decision.allowed is True

from agentcore.tools.knowledge_base import KnowledgeBaseTool


def test_exact_match():
    tool = KnowledgeBaseTool()
    result = tool.run(term="agentic ai")
    assert result.success is True
    assert "agent" in result.output.lower()


def test_fuzzy_match():
    tool = KnowledgeBaseTool()
    result = tool.run(term="retrieval augmented generaton")
    assert result.success is True


def test_missing_term():
    tool = KnowledgeBaseTool()
    result = tool.run(term="quantum toaster")
    assert result.success is False

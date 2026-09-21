from agentcore.tools.summarizer import TextSummarizerTool


def test_summary_shorter_than_source():
    tool = TextSummarizerTool()
    text = (
        "Agentic AI systems combine language models with tools. "
        "They can plan multi step tasks and call external functions. "
        "Responsible use requires guardrails and logging. "
        "Students should learn to evaluate agent behaviour critically."
    )
    result = tool.run(text=text, max_sentences=2)
    assert result.success is True
    assert len(result.output) < len(text)


def test_empty_text():
    tool = TextSummarizerTool()
    result = tool.run(text="", max_sentences=2)
    assert result.success is False

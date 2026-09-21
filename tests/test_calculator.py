from agentcore.tools.calculator import CalculatorTool


def test_addition():
    tool = CalculatorTool()
    result = tool.run(expression="2 + 3")
    assert result.success is True
    assert result.output == 5


def test_operator_precedence():
    tool = CalculatorTool()
    result = tool.run(expression="2 + 3 * 4")
    assert result.output == 14


def test_invalid_expression():
    tool = CalculatorTool()
    result = tool.run(expression="import os")
    assert result.success is False

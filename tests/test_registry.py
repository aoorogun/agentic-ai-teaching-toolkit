from agentcore.registry import ToolRegistry
from agentcore.tools.calculator import CalculatorTool


def test_register_and_dispatch():
    registry = ToolRegistry()
    registry.register(CalculatorTool())
    result = registry.dispatch("calculator", {"expression": "4 * 5"})
    assert result.output == 20


def test_list_specs():
    registry = ToolRegistry()
    registry.register(CalculatorTool())
    specs = registry.list_specs()
    assert specs[0]["name"] == "calculator"

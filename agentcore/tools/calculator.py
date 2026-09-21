from __future__ import annotations
import ast
import operator
from typing import Any
from agentcore.tools.base import Tool, ToolResult

_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def _evaluate(node: ast.AST) -> float:
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("unsupported_constant")
    if isinstance(node, ast.BinOp):
        operator_fn = _OPERATORS.get(type(node.op))
        if operator_fn is None:
            raise ValueError("unsupported_operator")
        return operator_fn(_evaluate(node.left), _evaluate(node.right))
    if isinstance(node, ast.UnaryOp):
        operator_fn = _OPERATORS.get(type(node.op))
        if operator_fn is None:
            raise ValueError("unsupported_operator")
        return operator_fn(_evaluate(node.operand))
    raise ValueError("unsupported_expression")


class CalculatorTool(Tool):
    name = "calculator"
    description = "Evaluates arithmetic expressions using +, -, *, /, **, % and parentheses."
    parameters = {
        "type": "object",
        "properties": {
            "expression": {"type": "string"}
        },
        "required": ["expression"],
    }

    def run(self, **kwargs: Any) -> ToolResult:
        expression = kwargs.get("expression", "")
        try:
            parsed = ast.parse(expression, mode="eval")
            value = _evaluate(parsed.body)
            return ToolResult(success=True, output=value)
        except Exception as exc:
            return ToolResult(success=False, output=None, error=str(exc))

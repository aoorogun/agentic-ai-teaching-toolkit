from __future__ import annotations
from typing import Any

from agentcore.tools.base import Tool, ToolResult

_LENGTH_TO_METERS = {
    "m": 1.0,
    "km": 1000.0,
    "cm": 0.01,
    "mm": 0.001,
    "mile": 1609.34,
    "foot": 0.3048,
    "inch": 0.0254,
}

_MASS_TO_GRAMS = {
    "g": 1.0,
    "kg": 1000.0,
    "mg": 0.001,
    "lb": 453.592,
    "oz": 28.3495,
}


def _normalize_unit(unit: str, table: dict) -> str:
    if unit in table:
        return unit
    singular = unit.rstrip("s")
    if singular in table:
        return singular
    return unit


def _convert_temperature(value: float, from_unit: str, to_unit: str) -> float:
    if from_unit == to_unit:
        return value
    if from_unit == "c" and to_unit == "f":
        return value * 9 / 5 + 32
    if from_unit == "f" and to_unit == "c":
        return (value - 32) * 5 / 9
    if from_unit == "c" and to_unit == "k":
        return value + 273.15
    if from_unit == "k" and to_unit == "c":
        return value - 273.15
    if from_unit == "f" and to_unit == "k":
        return (value - 32) * 5 / 9 + 273.15
    if from_unit == "k" and to_unit == "f":
        return (value - 273.15) * 9 / 5 + 32
    raise ValueError("unsupported_temperature_pair")


class UnitConverterTool(Tool):
    name = "unit_converter"
    description = "Converts values between length, mass and temperature units."
    parameters = {
        "type": "object",
        "properties": {
            "value": {"type": "number"},
            "from_unit": {"type": "string"},
            "to_unit": {"type": "string"},
        },
        "required": ["value", "from_unit", "to_unit"],
    }

    def run(self, **kwargs: Any) -> ToolResult:
        value = kwargs.get("value")
        from_unit = _normalize_unit(str(kwargs.get("from_unit", "")).lower(), _LENGTH_TO_METERS)
        to_unit = _normalize_unit(str(kwargs.get("to_unit", "")).lower(), _LENGTH_TO_METERS)
        from_unit = _normalize_unit(from_unit, _MASS_TO_GRAMS)
        to_unit = _normalize_unit(to_unit, _MASS_TO_GRAMS)
        try:
            value = float(value)
            if from_unit in _LENGTH_TO_METERS and to_unit in _LENGTH_TO_METERS:
                meters = value * _LENGTH_TO_METERS[from_unit]
                result = meters / _LENGTH_TO_METERS[to_unit]
                return ToolResult(success=True, output=result)
            if from_unit in _MASS_TO_GRAMS and to_unit in _MASS_TO_GRAMS:
                grams = value * _MASS_TO_GRAMS[from_unit]
                result = grams / _MASS_TO_GRAMS[to_unit]
                return ToolResult(success=True, output=result)
            if from_unit in {"c", "f", "k"} and to_unit in {"c", "f", "k"}:
                result = _convert_temperature(value, from_unit, to_unit)
                return ToolResult(success=True, output=result)
            raise ValueError("unsupported_unit_pair")
        except Exception as exc:
            return ToolResult(success=False, output=None, error=str(exc))

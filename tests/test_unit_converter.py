from agentcore.tools.unit_converter import UnitConverterTool


def test_length_conversion():
    tool = UnitConverterTool()
    result = tool.run(value=1, from_unit="km", to_unit="m")
    assert result.success is True
    assert result.output == 1000.0


def test_temperature_conversion():
    tool = UnitConverterTool()
    result = tool.run(value=0, from_unit="c", to_unit="f")
    assert round(result.output, 2) == 32.0


def test_plural_unit_name():
    tool = UnitConverterTool()
    result = tool.run(value=10, from_unit="miles", to_unit="km")
    assert result.success is True
    assert round(result.output, 2) == 16.09


def test_unsupported_pair():
    tool = UnitConverterTool()
    result = tool.run(value=1, from_unit="km", to_unit="c")
    assert result.success is False

from app.agents.tool_calling import create_tool


def test_search_logs_tool_definition():

    tool = create_tool()

    assert tool is not None
    assert tool.function_declarations is not None
    assert len(tool.function_declarations) == 1

    declaration = tool.function_declarations[0]

    assert declaration.name == "search_logs"
    assert "incident" in declaration.description.lower()

    assert "incident_id" in declaration.parameters.properties
    assert "level" in declaration.parameters.properties
    assert "keyword" in declaration.parameters.properties

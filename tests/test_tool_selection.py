from app.agents.tool_calling import create_tools


def test_all_expected_tools_are_available():

    tools = create_tools()

    declarations = tools[0].function_declarations

    names = {
        declaration.name
        for declaration in declarations
    }

    assert "search_logs" in names
    assert "extract_errors" in names
    assert "check_service_health" in names
    assert "get_incident_context" in names

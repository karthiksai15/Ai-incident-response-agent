from app.agents.tool_calling import create_tools


def test_multiple_tools_are_registered():

    tools = create_tools()

    assert len(tools) == 1

    declarations = tools[0].function_declarations

    names = {
        declaration.name
        for declaration in declarations
    }

    assert names == {
        "search_logs",
        "extract_errors",
        "check_service_health",
        "get_incident_context",
    }

from app.agents.tools import (
    SEARCH_LOGS_TOOL,
    execute_search_logs,
)


def test_search_logs_tool_schema():

    assert SEARCH_LOGS_TOOL["name"] == "search_logs"

    assert "description" in SEARCH_LOGS_TOOL

    parameters = SEARCH_LOGS_TOOL["parameters"]

    assert parameters["type"] == "object"

    properties = parameters["properties"]

    assert "incident_id" in properties
    assert "level" in properties
    assert "keyword" in properties

    assert "incident_id" in parameters["required"]


def test_execute_search_logs():

    results = execute_search_logs(
        incident_id="INC-001",
        level="ERROR",
    )

    assert len(results) > 0

    assert all(
        log.level == "ERROR"
        for log in results
    )

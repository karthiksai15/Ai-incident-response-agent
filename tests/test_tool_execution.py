from app.agents.tool_calling import search_logs_tool


def test_search_logs_tool_execution():

    results = search_logs_tool(
        incident_id="INC-001",
        level="ERROR",
    )

    assert len(results) > 0

    assert all(
        result["level"] == "ERROR"
        for result in results
    )

    messages = [
        result["message"]
        for result in results
    ]

    assert any(
        "connection" in message.lower()
        for message in messages
    )

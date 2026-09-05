from app.agents.state_updater import update_investigation_state


def build_state():
    return {
        "incident_id": "INC-001",
        "service": "payment-service",
        "severity": "HIGH",
        "logs": [],
        "evidence": [],
        "retrieved_knowledge": [],
        "similar_incidents": [],
        "root_cause": "",
        "confidence": 0.0,
        "recommendation": "",
        "investigation_notes": [],
        "current_goal": "",
        "completed_goals": [],
        "next_action": "retrieve_knowledge",
        "tools_used": [],
        "iteration": 3,
        "investigation_complete": False,
    }


def test_memory_availability_is_recorded():

    state = build_state()

    result = update_investigation_state(
        state,
        {
            "knowledge": [
                "Database connection pool runbook."
            ],
            "similar_incidents": [
                "Previous database pool exhaustion incident."
            ],
        },
    )

    assert result["similar_incidents"] == [
        "Previous database pool exhaustion incident."
    ]

    assert (
        "Relevant historical incidents were available "
        "as supporting evidence."
        in result["investigation_notes"]
    )


def test_missing_memory_is_recorded():

    state = build_state()

    result = update_investigation_state(
        state,
        {
            "knowledge": [
                "Database connection pool runbook."
            ],
            "similar_incidents": [],
        },
    )

    assert (
        "No relevant historical incidents were found."
        in result["investigation_notes"]
    )

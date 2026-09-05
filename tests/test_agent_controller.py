from app.agents import agent_controller


def build_state():
    return {
        "incident_id": "INC-001",
        "service": "payment-service",
        "severity": "HIGH",
        "logs": [],
        "evidence": [],
        "retrieved_knowledge": [],
        "root_cause": "",
        "confidence": 0.0,
        "recommendation": "",
        "investigation_notes": [],
        "current_goal": "",
        "completed_goals": [],
        "next_action": "",
        "tools_used": [],
        "iteration": 0,
        "investigation_complete": False,
    }


def fake_execute_decision(state):

    action = state["next_action"]

    if action == "get_incident_context":
        return {
            "incident_id": "INC-001",
            "service": "payment-service",
            "severity": "HIGH",
            "status": "OPEN",
            "log_count": 8,
        }

    if action == "check_service_health":
        return {
            "service": "payment-service",
            "status": "UNHEALTHY",
            "response_time_ms": 1250,
            "message": "Database connection issues",
        }

    if action == "extract_errors":
        return [
            {
                "message": "Timeout waiting for database connection",
            },
            {
                "message": "Connection pool exhausted",
            },
        ]

    if action == "retrieve_knowledge":
        return {
            "success": True,
            "knowledge": [
                "Database connection pool exhaustion can cause connection timeouts."
            ],
        }

    if action == "analyze_evidence":
        return {
            "root_cause": "Database connection pool exhaustion",
            "confidence": 0.95,
            "recommendation": (
                "Investigate database connections and connection leaks."
            ),
            "evidence": [
                "Connection pool exhausted",
                "Timeout waiting for database connection",
            ],
        }

    raise ValueError(
        f"Unexpected action: {action}"
    )


def test_agent_controller_completes_investigation(monkeypatch):

    monkeypatch.setattr(
        agent_controller,
        "execute_decision",
        fake_execute_decision,
    )

    state = build_state()

    result = agent_controller.run_agent_investigation(
        state,
        max_iterations=5,
    )

    assert result["investigation_complete"] is True

    assert result["root_cause"] == (
        "Database connection pool exhaustion"
    )

    assert result["confidence"] == 0.95

    assert result["recommendation"] != ""

    assert result["completed_goals"] == [
        "understand_context",
        "check_service_health",
        "collect_error_evidence",
        "retrieve_knowledge",
        "determine_root_cause",
    ]

    assert result["iteration"] == 5

    assert result["tools_used"] == [
        "get_incident_context",
        "check_service_health",
        "extract_errors",
        "retrieve_knowledge",
        "analyze_evidence",
    ]

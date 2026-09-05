from evaluation.runners.agent_adapter import (
    build_agent_state,
)


def test_build_agent_state_excludes_ground_truth():

    incident = {
        "incident_id": "EVAL-001",
        "service": "payment-service",
        "severity": "HIGH",
        "logs": [
            "Connection pool exhausted",
        ],
        "expected_root_cause": (
            "Database connection pool exhaustion"
        ),
        "expected_evidence": [
            "Connection pool exhausted",
        ],
    }

    state = build_agent_state(incident)

    assert state["incident_id"] == "EVAL-001"
    assert state["service"] == "payment-service"
    assert state["logs"] == [
        "Connection pool exhausted"
    ]

    assert "expected_root_cause" not in state
    assert "expected_evidence" not in state

from app.agents.investigation_goals import InvestigationGoal
from app.graph.state import IncidentState


def test_investigation_goals_exist():
    assert InvestigationGoal.UNDERSTAND_CONTEXT.value == "understand_context"
    assert InvestigationGoal.CHECK_SERVICE_HEALTH.value == "check_service_health"
    assert InvestigationGoal.COLLECT_ERROR_EVIDENCE.value == "collect_error_evidence"
    assert InvestigationGoal.SEARCH_LOG_EVIDENCE.value == "search_log_evidence"
    assert InvestigationGoal.RETRIEVE_KNOWLEDGE.value == "retrieve_knowledge"
    assert InvestigationGoal.DETERMINE_ROOT_CAUSE.value == "determine_root_cause"
    assert InvestigationGoal.PRODUCE_RECOMMENDATION.value == "produce_recommendation"


def test_state_contains_investigation_goals():
    state: IncidentState = {
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
        "current_goal": InvestigationGoal.CHECK_SERVICE_HEALTH.value,
        "completed_goals": [
            InvestigationGoal.UNDERSTAND_CONTEXT.value
        ],
        "next_action": "check_service_health",
        "tools_used": [
            "get_incident_context"
        ],
        "iteration": 1,
        "investigation_complete": False,
    }

    assert state["current_goal"] == "check_service_health"
    assert "understand_context" in state["completed_goals"]

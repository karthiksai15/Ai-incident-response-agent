from types import SimpleNamespace

from app.agents.analysis_executor import (
    analyze_investigation,
    analyze_memory_rag_investigation,
)
from app.agents.rag_executor import retrieve_incident_knowledge
from app.memory.knowledge_retrieval import retrieve_combined_knowledge
from app.agents.tool_calling import execute_tool_call
from app.graph.state import IncidentState


def execute_decision(state: IncidentState) -> object:
    """
    Execute the action selected by the investigation decision strategy.
    """

    action = state["next_action"]

    if action == "get_incident_context":
        arguments = {
            "incident_id": state["incident_id"],
            "service": state["service"],
            "severity": state["severity"],
        }

    elif action == "check_service_health":
        arguments = {
            "service": state["service"],
        }

    elif action == "extract_errors":
        arguments = {
            "incident_id": state["incident_id"],
        }

    elif action == "search_logs":
        arguments = {
            "incident_id": state["incident_id"],
        }

    elif action == "retrieve_knowledge":
        context = retrieve_combined_knowledge(
            service=state["service"],
            severity=state["severity"],
            evidence=state["evidence"],
            top_k=3,
        )

        return {
            "success": True,
            "knowledge": context.runbooks,
            "similar_incidents": context.similar_incidents,
        }

    elif action == "analyze_evidence":
        analysis = analyze_memory_rag_investigation(
            incident_id=state["incident_id"],
            service=state["service"],
            severity=state["severity"],
            evidence=state["evidence"],
            runbooks=state["retrieved_knowledge"],
            similar_incidents=state["similar_incidents"],
        )

        return {
            "root_cause": analysis.root_cause,
            "confidence": analysis.confidence,
            "recommendation": analysis.recommendation,
            "evidence": analysis.evidence,
        }

    else:
        raise ValueError(
            f"Unsupported action: {action}"
        )

    function_call = SimpleNamespace(
        name=action,
        args=arguments,
    )

    return execute_tool_call(function_call)


def execute_memory_rag_decision(
    state: IncidentState,
) -> object:
    """
    Retrieve both official runbooks and similar historical incidents.
    """

    context = retrieve_combined_knowledge(
        service=state["service"],
        severity=state["severity"],
        evidence=state["evidence"],
        top_k=3,
    )

    return {
        "success": True,
        "knowledge": context.runbooks,
        "similar_incidents": context.similar_incidents,
    }

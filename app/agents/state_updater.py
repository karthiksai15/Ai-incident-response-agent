from app.agents.investigation_goals import InvestigationGoal
from app.graph.state import IncidentState


def update_investigation_state(
    state: IncidentState,
    tool_result,
) -> IncidentState:
    """
    Update investigation state using the result
    produced by the selected action.
    """

    action = state["next_action"]

    completed_goals = list(
        state["completed_goals"]
    )

    tools_used = list(
        state["tools_used"]
    )

    investigation_notes = list(
        state["investigation_notes"]
    )

    if action not in tools_used:
        tools_used.append(action)

    if action == "get_incident_context":
        goal = InvestigationGoal.UNDERSTAND_CONTEXT.value

        if goal not in completed_goals:
            completed_goals.append(goal)

        investigation_notes.append(
            "Incident context retrieved successfully."
        )

    elif action == "check_service_health":
        goal = InvestigationGoal.CHECK_SERVICE_HEALTH.value

        if goal not in completed_goals:
            completed_goals.append(goal)

        investigation_notes.append(
            "Service health checked successfully."
        )

    elif action == "extract_errors":
        goal = InvestigationGoal.COLLECT_ERROR_EVIDENCE.value

        if goal not in completed_goals:
            completed_goals.append(goal)

        if isinstance(tool_result, list):
            evidence = []

            for log in tool_result:
                if isinstance(log, dict):
                    message = log.get("message")

                    if message:
                        evidence.append(message)

            state["evidence"] = evidence

        investigation_notes.append(
            "Error evidence collected successfully."
        )

    elif action == "search_logs":
        goal = InvestigationGoal.SEARCH_LOG_EVIDENCE.value

        if goal not in completed_goals:
            completed_goals.append(goal)

        if isinstance(tool_result, list):
            logs = []

            for log in tool_result:
                if isinstance(log, dict):
                    message = log.get("message")

                    if message:
                        logs.append(message)

            state["logs"] = logs

        investigation_notes.append(
            "Log evidence searched successfully."
        )

    elif action == "retrieve_knowledge":
        goal = InvestigationGoal.RETRIEVE_KNOWLEDGE.value

        if goal not in completed_goals:
            completed_goals.append(goal)

        if isinstance(tool_result, dict):
            knowledge = tool_result.get(
                "knowledge",
                []
            )

            state["retrieved_knowledge"] = knowledge
            state["similar_incidents"] = tool_result.get(
                "similar_incidents",
                []
            )

        investigation_notes.append(
            "Relevant operational knowledge retrieved."
        )

        if state["similar_incidents"]:
            investigation_notes.append(
                "Relevant historical incidents were available "
                "as supporting evidence."
            )
        else:
            investigation_notes.append(
                "No relevant historical incidents were found."
            )

    elif action == "analyze_evidence":
        goal = InvestigationGoal.DETERMINE_ROOT_CAUSE.value

        if goal not in completed_goals:
            completed_goals.append(goal)

        if not isinstance(tool_result, dict):
            raise ValueError(
                "Analysis result must be a dictionary"
            )

        state["root_cause"] = tool_result.get(
            "root_cause",
            ""
        )

        state["confidence"] = tool_result.get(
            "confidence",
            0.0
        )

        state["recommendation"] = tool_result.get(
            "recommendation",
            ""
        )

        investigation_notes.append(
            "Incident analysis completed using Gemini."
        )

    else:
        raise ValueError(
            f"Unsupported state update action: {action}"
        )

    state["completed_goals"] = completed_goals
    state["tools_used"] = tools_used
    state["investigation_notes"] = investigation_notes

    state["iteration"] += 1

    return state

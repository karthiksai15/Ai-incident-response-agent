from app.agents.investigation_goals import InvestigationGoal


GOAL_SEQUENCE = [
    InvestigationGoal.UNDERSTAND_CONTEXT.value,
    InvestigationGoal.CHECK_SERVICE_HEALTH.value,
    InvestigationGoal.COLLECT_ERROR_EVIDENCE.value,
    InvestigationGoal.RETRIEVE_KNOWLEDGE.value,
    InvestigationGoal.DETERMINE_ROOT_CAUSE.value,
]


GOAL_TO_ACTION = {
    InvestigationGoal.UNDERSTAND_CONTEXT.value:
        "get_incident_context",

    InvestigationGoal.CHECK_SERVICE_HEALTH.value:
        "check_service_health",

    InvestigationGoal.COLLECT_ERROR_EVIDENCE.value:
        "extract_errors",

    InvestigationGoal.SEARCH_LOG_EVIDENCE.value:
        "search_logs",

    InvestigationGoal.RETRIEVE_KNOWLEDGE.value:
        "retrieve_knowledge",

    InvestigationGoal.DETERMINE_ROOT_CAUSE.value:
        "analyze_evidence",

    InvestigationGoal.PRODUCE_RECOMMENDATION.value:
        "analyze_evidence",
}


def choose_next_action(current_goal: str) -> str:
    if not isinstance(current_goal, str):
        raise ValueError(
            "current_goal must be a string"
        )

    current_goal = current_goal.strip()

    if not current_goal:
        raise ValueError(
            "current_goal cannot be empty"
        )

    action = GOAL_TO_ACTION.get(current_goal)

    if action is None:
        raise ValueError(
            f"Unknown investigation goal: {current_goal}"
        )

    return action


def decide_next_goal(
    completed_goals: list[str],
) -> str:

    if not isinstance(completed_goals, list):
        raise ValueError(
            "completed_goals must be a list"
        )

    for goal in GOAL_SEQUENCE:
        if goal not in completed_goals:
            return goal

    return ""


def decide_next_action(
    completed_goals: list[str],
) -> str:

    next_goal = decide_next_goal(
        completed_goals
    )

    if not next_goal:
        return ""

    return choose_next_action(
        next_goal
    )


def has_relevant_memory(similar_incidents: list[str]) -> bool:
    """
    Determine whether relevant historical incidents are available
    for the current investigation.
    """

    if not isinstance(similar_incidents, list):
        raise ValueError(
            "similar_incidents must be a list"
        )

    return any(
        isinstance(incident, str) and incident.strip()
        for incident in similar_incidents
    )


def build_memory_context(
    similar_incidents: list[str],
) -> str:
    """
    Describe whether historical incident memory is available
    for the current investigation.
    """

    if not isinstance(similar_incidents, list):
        raise ValueError(
            "similar_incidents must be a list"
        )

    if any(
        isinstance(incident, str) and incident.strip()
        for incident in similar_incidents
    ):
        return (
            "Relevant historical incidents are available "
            "as supporting evidence."
        )

    return (
        "No relevant historical incidents are available."
    )

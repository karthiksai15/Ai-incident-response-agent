from app.agents.investigation_goals import InvestigationGoal
from app.graph.state import IncidentState


def should_stop_investigation(
    state: IncidentState,
) -> bool:
    """
    Determine whether the investigation has
    reached a logical completion point.
    """

    completed_goals = set(
        state["completed_goals"]
    )

    recommendation_goal = (
        InvestigationGoal.PRODUCE_RECOMMENDATION.value
    )

    if recommendation_goal in completed_goals:
        return True

    root_cause = state.get(
        "root_cause",
        ""
    )

    recommendation = state.get(
        "recommendation",
        ""
    )

    if (
        isinstance(root_cause, str)
        and root_cause.strip()
        and isinstance(recommendation, str)
        and recommendation.strip()
    ):
        return True

    return False

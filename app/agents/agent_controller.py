from app.agents.decision_executor import execute_decision
from app.agents.decision_strategy import (
    choose_next_action,
    decide_next_goal,
)
from app.agents.iteration_safety import (
    has_reached_max_iterations,
)
from app.agents.state_updater import (
    update_investigation_state,
)
from app.agents.stopping_conditions import (
    should_stop_investigation,
)
from app.graph.state import IncidentState


def run_agent_investigation(
    state: IncidentState,
    max_iterations: int = 5,
) -> IncidentState:

    while True:

        if should_stop_investigation(state):
            state["investigation_complete"] = True
            return state

        if has_reached_max_iterations(
            state,
            max_iterations=max_iterations,
        ):
            state["investigation_complete"] = True
            state["investigation_notes"].append(
                "Investigation stopped because the maximum iteration limit was reached."
            )
            return state

        next_goal = decide_next_goal(
            state["completed_goals"]
        )

        if not next_goal:
            state["investigation_complete"] = True
            return state

        state["current_goal"] = next_goal

        state["next_action"] = choose_next_action(
            next_goal
        )

        tool_result = execute_decision(
            state
        )

        state = update_investigation_state(
            state,
            tool_result,
        )

from app.graph.state import IncidentState


DEFAULT_MAX_ITERATIONS = 5


def has_reached_max_iterations(
    state: IncidentState,
    max_iterations: int = DEFAULT_MAX_ITERATIONS,
) -> bool:
    """
    Determine whether the investigation has reached
    its maximum allowed number of iterations.
    """

    if not isinstance(max_iterations, int):
        raise ValueError(
            "max_iterations must be an integer"
        )

    if max_iterations <= 0:
        raise ValueError(
            "max_iterations must be greater than 0"
        )

    return state["iteration"] >= max_iterations

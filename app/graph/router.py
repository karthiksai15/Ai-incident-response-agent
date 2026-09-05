from app.graph.state import IncidentState


def route_after_evidence(state: IncidentState) -> str:
    if state["evidence"]:
        return "retrieve_knowledge"

    return "manual_investigation"

from app.graph.state import IncidentState
from app.tools.log_search import search_logs


def search_error_logs(state: IncidentState):
    logs = search_logs(
        incident_id=state["incident_id"],
        level="ERROR",
    )

    evidence = [
        log.message
        for log in logs
    ]

    return {
        "evidence": evidence,
        "investigation_notes": [
            "ERROR logs retrieved using search_logs tool."
        ],
    }

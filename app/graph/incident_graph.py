from langgraph.graph import END, START, StateGraph

from app.graph.analysis_node import analyze_evidence

from app.graph.nodes import (
    load_incident,
    retrieve_knowledge,
)

from app.graph.tool_nodes import search_error_logs

from app.graph.state import IncidentState


graph_builder = StateGraph(IncidentState)


graph_builder.add_node(
    "load_incident",
    load_incident,
)

graph_builder.add_node(
    "search_error_logs",
    search_error_logs,
)

graph_builder.add_node(
    "retrieve_knowledge",
    retrieve_knowledge,
)

graph_builder.add_node(
    "analyze_evidence",
    analyze_evidence,
)


graph_builder.add_edge(
    START,
    "load_incident",
)

graph_builder.add_edge(
    "load_incident",
    "search_error_logs",
)

graph_builder.add_edge(
    "search_error_logs",
    "retrieve_knowledge",
)

graph_builder.add_edge(
    "retrieve_knowledge",
    "analyze_evidence",
)

graph_builder.add_edge(
    "analyze_evidence",
    END,
)


incident_graph = graph_builder.compile()


if __name__ == "__main__":
    initial_state: IncidentState = {
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
    }

    result = incident_graph.invoke(
        initial_state
    )

    print("\n=== Incident Investigation Graph ===")

    print(
        f"Incident: {result['incident_id']}"
    )

    print(
        f"Logs: {len(result['logs'])}"
    )

    print(
        f"Evidence: {len(result['evidence'])}"
    )

    print(
        f"Knowledge chunks: "
        f"{len(result['retrieved_knowledge'])}"
    )

    print(
        f"Root Cause: "
        f"{result['root_cause']}"
    )

    print(
        f"Confidence: "
        f"{result['confidence']:.2f}"
    )

    print(
        f"Recommendation: "
        f"{result['recommendation']}"
    )

    print("\nInvestigation Notes:")

    for note in result["investigation_notes"]:
        print(f"- {note}")

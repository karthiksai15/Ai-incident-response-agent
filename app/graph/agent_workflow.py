from langgraph.graph import END, START, StateGraph

from app.agents.agent_controller import run_agent_investigation
from app.graph.state import IncidentState


def run_investigation(state: IncidentState):
    return run_agent_investigation(
        state=state,
        max_iterations=5,
    )


graph_builder = StateGraph(IncidentState)

graph_builder.add_node(
    "run_investigation",
    run_investigation,
)

graph_builder.add_edge(
    START,
    "run_investigation",
)

graph_builder.add_edge(
    "run_investigation",
    END,
)

agent_workflow = graph_builder.compile()

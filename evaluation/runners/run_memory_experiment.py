import json

from evaluation.runners.configurations import (
    ExperimentConfiguration,
)
from evaluation.runners.evaluation_runner import (
    load_evaluation_dataset,
)
from evaluation.runners.experiment import (
    run_single_experiment,
)
from app.memory.runbook_retrieval import (
    retrieve_runbook_knowledge,
)
from app.memory.retrieval import (
    retrieve_similar_incidents,
)


dataset = load_evaluation_dataset()

incident = next(
    item
    for item in dataset
    if item["incident_id"] == "EVAL-001"
)

runbooks = retrieve_runbook_knowledge(
    service=incident["service"],
    severity=incident["severity"],
    evidence=incident["logs"],
    top_k=1,
)

memories = retrieve_similar_incidents(
    service=incident["service"],
    severity=incident["severity"],
    evidence=incident["logs"],
    top_k=1,
)

similar_incidents = [
    memory["document"]
    for memory in memories
]

print("\n--- RETRIEVED MEMORY ---")
for memory in similar_incidents:
    print(memory)

result = run_single_experiment(
    incident=incident,
    configuration=(
        ExperimentConfiguration.RAG_MEMORY
    ),
    runbooks=runbooks,
    similar_incidents=similar_incidents,
)

print("\n--- EXPERIMENT RESULT ---")
print(json.dumps(result, indent=2))

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

result = run_single_experiment(
    incident=incident,
    configuration=ExperimentConfiguration.RAG,
    runbooks=runbooks,
    similar_incidents=[],
)

print(json.dumps(result, indent=2))

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


dataset = load_evaluation_dataset()

incident = next(
    item
    for item in dataset
    if item["incident_id"] == "EVAL-001"
)

result = run_single_experiment(
    incident=incident,
    configuration=ExperimentConfiguration.LLM_ONLY,
)

print(json.dumps(result, indent=2))

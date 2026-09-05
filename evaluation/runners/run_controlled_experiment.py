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


CONFIGURATIONS = [
    ExperimentConfiguration.LLM_ONLY,
    ExperimentConfiguration.RAG,
    ExperimentConfiguration.RAG_MEMORY,
]


def run_experiment():
    dataset = load_evaluation_dataset()
    results = []

    for incident in dataset:

        print(
            f"\n=== {incident['incident_id']} ==="
        )

        runbooks = []
        memories = []

        if (
            ExperimentConfiguration.RAG
            in CONFIGURATIONS
        ):
            runbooks = retrieve_runbook_knowledge(
                service=incident["service"],
                severity=incident["severity"],
                evidence=incident["logs"],
                top_k=1,
            )

        if (
            ExperimentConfiguration.RAG_MEMORY
            in CONFIGURATIONS
        ):
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

        for configuration in CONFIGURATIONS:

            print(
                f"Running {configuration.value}..."
            )

            result = run_single_experiment(
                incident=incident,
                configuration=configuration,
                runbooks=(
                    runbooks
                    if configuration
                    in [
                        ExperimentConfiguration.RAG,
                        ExperimentConfiguration.RAG_MEMORY,
                    ]
                    else []
                ),
                similar_incidents=(
                    similar_incidents
                    if configuration
                    == ExperimentConfiguration.RAG_MEMORY
                    else []
                ),
            )

            results.append(result)

            print(
                json.dumps(
                    result,
                    indent=2,
                )
            )

    with open(
        "evaluation/results/controlled_experiment.json",
        "w",
    ) as file:
        json.dump(
            results,
            file,
            indent=2,
        )


if __name__ == "__main__":
    run_experiment()

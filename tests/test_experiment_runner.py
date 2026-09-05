from evaluation.runners.configurations import (
    ExperimentConfiguration,
)
from evaluation.runners.experiment_runner import (
    get_configuration_description,
)


def test_experiment_runner_supports_all_configurations():

    assert "without RAG" in (
        get_configuration_description(
            ExperimentConfiguration.LLM_ONLY
        )
    )

    assert "official runbook RAG" in (
        get_configuration_description(
            ExperimentConfiguration.RAG
        )
    )

    assert "historical memory" in (
        get_configuration_description(
            ExperimentConfiguration.RAG_MEMORY
        )
    )

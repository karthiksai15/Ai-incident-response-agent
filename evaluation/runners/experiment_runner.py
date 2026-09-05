from evaluation.runners.configurations import (
    ExperimentConfiguration,
)


def validate_configuration(
    configuration: ExperimentConfiguration,
) -> ExperimentConfiguration:
    """
    Validate and return an experiment configuration.
    """

    if not isinstance(
        configuration,
        ExperimentConfiguration,
    ):
        raise ValueError(
            "Invalid experiment configuration"
        )

    return configuration


def get_configuration_description(
    configuration: ExperimentConfiguration,
) -> str:

    configuration = validate_configuration(
        configuration
    )

    descriptions = {
        ExperimentConfiguration.LLM_ONLY:
            "LLM analysis without RAG or memory",

        ExperimentConfiguration.RAG:
            "LLM analysis with official runbook RAG",

        ExperimentConfiguration.RAG_MEMORY:
            "LLM analysis with runbooks and historical memory",
    }

    return descriptions[configuration]

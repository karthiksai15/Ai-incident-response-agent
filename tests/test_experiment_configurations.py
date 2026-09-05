from evaluation.runners.configurations import (
    ExperimentConfiguration,
)


def test_experiment_configurations():

    assert (
        ExperimentConfiguration.LLM_ONLY.value
        == "llm_only"
    )

    assert (
        ExperimentConfiguration.RAG.value
        == "llm_rag"
    )

    assert (
        ExperimentConfiguration.RAG_MEMORY.value
        == "llm_rag_memory"
    )

from enum import Enum


class ExperimentConfiguration(str, Enum):
    LLM_ONLY = "llm_only"
    RAG = "llm_rag"
    RAG_MEMORY = "llm_rag_memory"

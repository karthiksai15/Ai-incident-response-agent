from app.rag.embeddings import EmbeddingModel


def create_memory_text(
    service: str,
    severity: str,
    root_cause: str,
    evidence: list[str],
) -> str:

    evidence_text = " ".join(evidence)

    return (
        f"Service: {service}\n"
        f"Severity: {severity}\n"
        f"Root Cause: {root_cause}\n"
        f"Evidence: {evidence_text}"
    )


def create_memory_embedding(text: str) -> list[float]:
    embedding_model = EmbeddingModel()
    return embedding_model.embed_text(text)

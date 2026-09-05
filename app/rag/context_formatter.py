from app.rag.context import RAGContext


def format_rag_context(
    context: RAGContext,
) -> str:
    """
    Convert a structured RAG context into
    readable text for an analyzer or LLM.
    """

    lines = []

    lines.append("INCIDENT")
    lines.append(
        f"Incident ID: {context.incident_id}"
    )
    lines.append(
        f"Service: {context.service}"
    )
    lines.append(
        f"Severity: {context.severity}"
    )

    lines.append("")
    lines.append("EVIDENCE")

    for log in context.evidence:
        lines.append(
            f"{log.timestamp} | "
            f"{log.level} | "
            f"{log.service} | "
            f"{log.message}"
        )

    lines.append("")
    lines.append("RETRIEVED KNOWLEDGE")

    for chunk in context.retrieved_knowledge:
        lines.append(
            f"Source: {chunk.source}"
        )
        lines.append(
            f"Chunk: {chunk.chunk_index}"
        )
        lines.append(
            chunk.content
        )
        lines.append("")

    return "\n".join(lines).strip()

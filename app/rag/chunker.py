from pydantic import BaseModel

from app.rag.document_loader import Document


class DocumentChunk(BaseModel):
    content: str
    source: str
    chunk_index: int
    metadata: dict[str, str]


def chunk_document(
    document: Document,
    chunk_size: int = 800,
    overlap: int = 100,
) -> list[DocumentChunk]:
    """
    Split a document into overlapping text chunks.
    """

    if chunk_size <= 0:
        raise ValueError(
            "chunk_size must be greater than 0"
        )

    if overlap < 0:
        raise ValueError(
            "overlap cannot be negative"
        )

    if overlap >= chunk_size:
        raise ValueError(
            "overlap must be smaller than chunk_size"
        )

    text = document.content

    chunks = []

    start = 0
    chunk_index = 0

    while start < len(text):
        end = start + chunk_size

        chunk_text = text[start:end].strip()

        if chunk_text:
            chunks.append(
                DocumentChunk(
                    content=chunk_text,
                    source=document.source,
                    chunk_index=chunk_index,
                    metadata=document.metadata.copy(),
                )
            )

            chunk_index += 1

        start = end - overlap

    return chunks


def chunk_documents(
    documents: list[Document],
    chunk_size: int = 800,
    overlap: int = 100,
) -> list[DocumentChunk]:
    """
    Chunk multiple documents.
    """

    chunks = []

    for document in documents:
        chunks.extend(
            chunk_document(
                document=document,
                chunk_size=chunk_size,
                overlap=overlap,
            )
        )

    return chunks

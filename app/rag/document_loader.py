from pathlib import Path

from pydantic import BaseModel

from app.core.config import BASE_DIR


class Document(BaseModel):
    content: str
    source: str
    metadata: dict[str, str]


RUNBOOK_DIRECTORY = BASE_DIR / "knowledge" / "runbooks"


def load_document(file_path: Path) -> Document:
    """
    Load a single Markdown document.
    """

    if not file_path.exists():
        raise FileNotFoundError(
            f"Document not found: {file_path}"
        )

    if file_path.suffix.lower() != ".md":
        raise ValueError(
            "Only Markdown documents are supported"
        )

    content = file_path.read_text(encoding="utf-8").strip()

    if not content:
        raise ValueError(
            f"Document is empty: {file_path.name}"
        )

    return Document(
        content=content,
        source=file_path.name,
        metadata={
            "type": "runbook",
            "format": "markdown",
        },
    )


def load_runbooks() -> list[Document]:
    """
    Load all Markdown runbooks from the runbook directory.
    """

    if not RUNBOOK_DIRECTORY.exists():
        raise FileNotFoundError(
            f"Runbook directory not found: {RUNBOOK_DIRECTORY}"
        )

    documents = []

    for file_path in sorted(RUNBOOK_DIRECTORY.glob("*.md")):
        documents.append(load_document(file_path))

    return documents

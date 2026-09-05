import json
from pathlib import Path

from app.memory.embedding import (
    create_memory_embedding,
    create_memory_text,
)
from app.memory.vector_store import (
    IncidentMemoryVectorStore,
)


DATASET_PATH = Path(
    "evaluation/dataset/historical_memories.json"
)


def seed_memories():
    with DATASET_PATH.open() as file:
        memories = json.load(file)

    store = IncidentMemoryVectorStore()

    for memory in memories:
        text = create_memory_text(
            service=memory["service"],
            severity=memory["severity"],
            root_cause=memory["root_cause"],
            evidence=memory["evidence"],
        )

        embedding = create_memory_embedding(text)

        store.add_memory(
            incident_id=memory["incident_id"],
            text=text,
            embedding=embedding,
            metadata={
                "service": memory["service"],
                "severity": memory["severity"],
                "status": "RESOLVED",
            },
        )

        print(
            f"Seeded {memory['incident_id']}"
        )


if __name__ == "__main__":
    seed_memories()

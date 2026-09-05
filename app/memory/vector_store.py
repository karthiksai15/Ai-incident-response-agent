import chromadb


class IncidentMemoryVectorStore:

    def __init__(self):
        self.client = chromadb.PersistentClient(
            path="data/chroma"
        )

        self.collection = self.client.get_or_create_collection(
            name="incident_memories"
        )

    def add_memory(
        self,
        incident_id: str,
        text: str,
        embedding: list[float],
        metadata: dict,
    ) -> None:

        self.collection.upsert(
            ids=[incident_id],
            documents=[text],
            embeddings=[embedding],
            metadatas=[metadata],
        )

    def search(
        self,
        embedding: list[float],
        top_k: int = 3,
    ) -> list[dict]:

        results = self.collection.query(
            query_embeddings=[embedding],
            n_results=top_k,
        )

        memories = []

        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]
        ids = results.get("ids", [[]])[0]

        for incident_id, document, metadata, distance in zip(
            ids,
            documents,
            metadatas,
            distances,
        ):
            memories.append(
                {
                    "incident_id": incident_id,
                    "document": document,
                    "metadata": metadata,
                    "distance": distance,
                }
            )

        return memories

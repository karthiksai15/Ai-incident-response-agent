import json

from app.memory.database import get_database_connection
from app.models.memory import IncidentMemory


def save_memory(memory: IncidentMemory) -> None:
    query = """
        INSERT INTO incident_memory (
            incident_id,
            service,
            severity,
            root_cause,
            confidence,
            evidence,
            recommendation,
            investigation_notes,
            status,
            created_at
        )
        VALUES (
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s
        )
        ON CONFLICT (incident_id) DO NOTHING
    """

    with get_database_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                query,
                (
                    memory.incident_id,
                    memory.service,
                    memory.severity,
                    memory.root_cause,
                    memory.confidence,
                    json.dumps(memory.evidence),
                    memory.recommendation,
                    json.dumps(memory.investigation_notes),
                    memory.status,
                    memory.created_at,
                ),
            )

        connection.commit()

from pydantic import BaseModel


class KnowledgeContext(BaseModel):
    runbooks: list[str]
    similar_incidents: list[str]

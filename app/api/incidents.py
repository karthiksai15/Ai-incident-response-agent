from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.incident_ingestion import ingest_incident


router = APIRouter(
    prefix="/incidents",
    tags=["Incidents"],
)


class IncidentIngestionRequest(BaseModel):
    incident_id: str
    service: str
    severity: str


@router.post("/")
def create_incident(request: IncidentIngestionRequest):

    try:
        incident = ingest_incident(
            incident_id=request.incident_id,
            service=request.service,
            severity=request.severity,
        )

        return incident

    except FileNotFoundError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error),
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

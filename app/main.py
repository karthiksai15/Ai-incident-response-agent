from fastapi import FastAPI

from app.api.incidents import router as incident_router


app = FastAPI(
    title="AI Incident Response Agent",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "ai-incident-response-agent",
    }


app.include_router(incident_router)

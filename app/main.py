from fastapi import FastAPI

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


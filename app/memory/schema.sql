CREATE TABLE IF NOT EXISTS incident_memory (
    id BIGSERIAL PRIMARY KEY,

    incident_id VARCHAR(100) NOT NULL UNIQUE,
    service VARCHAR(100) NOT NULL,
    severity VARCHAR(50) NOT NULL,

    root_cause TEXT NOT NULL,
    confidence DOUBLE PRECISION NOT NULL,

    evidence JSONB NOT NULL,
    recommendation TEXT NOT NULL,

    investigation_notes JSONB NOT NULL,

    status VARCHAR(50) NOT NULL,

    created_at TIMESTAMP NOT NULL
);

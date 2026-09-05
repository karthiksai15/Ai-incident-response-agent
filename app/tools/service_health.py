from pydantic import BaseModel

from app.tools.validation import validate_service


class ServiceHealth(BaseModel):
    service: str
    status: str
    response_time_ms: int
    message: str


SERVICE_STATUS = {
    "payment-service": {
        "status": "UNHEALTHY",
        "response_time_ms": 1250,
        "message": "Service is experiencing database connection issues",
    },
    "auth-service": {
        "status": "HEALTHY",
        "response_time_ms": 120,
        "message": "Service is operating normally",
    },
}


def check_service_health(service: str) -> ServiceHealth:
    """
    Check the health of a service.
    """

    service = validate_service(service)

    service_info = SERVICE_STATUS.get(service)

    if service_info is None:
        return ServiceHealth(
            service=service,
            status="UNKNOWN",
            response_time_ms=0,
            message="Service is not registered in the health simulator",
        )

    return ServiceHealth(
        service=service,
        status=service_info["status"],
        response_time_ms=service_info["response_time_ms"],
        message=service_info["message"],
    )

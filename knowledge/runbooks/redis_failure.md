# Redis Failure

## Problem

The application cannot communicate with Redis or Redis is responding
with excessive latency.

## Possible Causes

- Redis service is unavailable
- Redis connection failure
- Redis memory exhaustion
- Network connectivity problems
- Redis configuration issues
- Excessive Redis traffic
- Redis restart or failure

## Investigation

1. Check Redis service health.
2. Check Redis response latency.
3. Check Redis memory usage.
4. Check application logs for Redis connection errors.
5. Check recent Redis configuration or deployment changes.
6. Check network connectivity between the application and Redis.

## Evidence

Strong indicators include:

- Redis connection refused
- Redis timeout
- Redis unavailable
- Redis request latency increased
- Failed Redis operations

## Recommended Remediation

- Verify Redis availability.
- Restart Redis only according to operational policy.
- Investigate memory exhaustion.
- Check Redis configuration.
- Reduce excessive traffic if applicable.
- Restore connectivity between the application and Redis.

## Severity Guidance

HIGH severity may be appropriate when Redis failure affects
authentication, rate limiting, caching, or other critical operations.

## Related Services

- auth-service
- api-gateway

## Keywords

redis
cache
connection
timeout
memory
unavailable
latency

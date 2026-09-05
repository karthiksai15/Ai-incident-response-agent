# High API Latency

## Problem

API requests are taking significantly longer than the expected response
time threshold.

## Possible Causes

- Slow database queries
- Database connection pool exhaustion
- External service latency
- CPU saturation
- Memory pressure
- Network latency
- Excessive application traffic
- Inefficient application processing

## Investigation

1. Check API response time metrics.
2. Check application logs for slow requests.
3. Check database response time.
4. Check database connection pool utilization.
5. Check CPU and memory usage.
6. Check dependent service health.
7. Compare current traffic with normal traffic.
8. Check recent deployments or configuration changes.

## Evidence

Strong indicators include:

- Request latency exceeding threshold
- Increased response time across requests
- Database timeout errors
- Slow database queries
- Dependent service timeouts

## Recommended Remediation

- Identify the slowest dependency.
- Investigate slow database queries.
- Resolve connection pool issues.
- Scale the affected service when appropriate.
- Reduce unnecessary processing.
- Restore unhealthy dependencies.

## Severity Guidance

HIGH severity may be appropriate when latency affects critical
user-facing operations or causes significant request failures.

## Related Services

- payment-service
- auth-service
- api-gateway

## Keywords

latency
slow
response time
timeout
performance
database
traffic

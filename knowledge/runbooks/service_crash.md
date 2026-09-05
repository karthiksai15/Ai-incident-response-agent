# Service Crash

## Problem

A service has stopped running unexpectedly or is repeatedly restarting.

## Possible Causes

- Unhandled application exception
- Out-of-memory condition
- Invalid configuration
- Dependency failure
- Deployment problem
- Container failure
- Resource exhaustion

## Investigation

1. Check service health.
2. Check application logs around the crash time.
3. Identify the final ERROR or exception before termination.
4. Check CPU and memory usage.
5. Check recent deployments.
6. Check configuration changes.
7. Check dependent services.
8. Determine whether the service is repeatedly restarting.

## Evidence

Strong indicators include:

- Service unavailable
- Process terminated unexpectedly
- Container restart
- Out-of-memory error
- Unhandled exception
- Repeated health-check failures

## Recommended Remediation

- Identify the error that caused termination.
- Fix application or configuration issues.
- Restore failed dependencies.
- Restart the service when operational policy permits.
- Monitor the service after recovery.
- Investigate repeated crashes before returning the service to normal
  operation.

## Severity Guidance

CRITICAL severity may be appropriate when a critical service is
completely unavailable and business operations are blocked.

## Related Services

All application services.

## Keywords

crash
service unavailable
restart
exception
container
out-of-memory
health check
failure

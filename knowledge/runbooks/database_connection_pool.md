# Database Connection Pool Exhaustion

## Problem

The application cannot acquire a database connection because all
connections in the connection pool are currently in use.

Typical symptoms include:

- Connection pool exhausted
- Timeout waiting for database connection
- Failed to acquire JDBC connection
- Database request timeouts
- Increased application latency
- Failed application requests

## Possible Causes

- Too many concurrent requests
- Database connections are not being released
- Connection leaks in application code
- Database is responding slowly
- Database is unavailable
- Connection pool size is too small
- Long-running database queries
- Sudden increase in application traffic

## Investigation

1. Check the application connection pool utilization.
2. Check the number of active database connections.
3. Check database response time.
4. Check for long-running database queries.
5. Check application logs for connection timeout errors.
6. Check whether a recent deployment changed database behavior.
7. Check whether application traffic increased unexpectedly.

## Evidence

Strong indicators of connection pool exhaustion include:

- Connection pool exhausted
- Timeout waiting for database connection
- Failed to acquire JDBC connection
- Multiple requests experiencing database timeouts

## Recommended Remediation

- Identify and fix connection leaks.
- Investigate long-running database queries.
- Verify database availability.
- Increase connection pool size only when justified by workload.
- Restart the affected service if it is unhealthy and operational policy
  permits a restart.
- Monitor connection pool utilization after remediation.

## Severity Guidance

HIGH severity may be appropriate when payment or critical business
requests are failing because database connections cannot be acquired.

## Related Services

- payment-service
- auth-service

## Keywords

database
postgresql
connection
connection pool
pool exhausted
jdbc
timeout
database latency

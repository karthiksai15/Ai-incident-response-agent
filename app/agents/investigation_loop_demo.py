from app.agents.tool_calling import run_investigation_loop


def main():

    prompt = """
You are investigating production incident INC-001.

Service: payment-service
Severity: HIGH

Investigate this incident systematically.

Use the available operational tools whenever
current operational evidence is needed.

You should:
1. Understand the incident context.
2. Check the service health.
3. Inspect relevant error logs.
4. Search logs for useful evidence if necessary.
5. Determine the most likely root cause.
6. Provide the important evidence.
7. Provide a practical recommendation.

Do not invent logs, metrics, or system behavior.

Continue investigating until you have enough
evidence to provide a reliable final analysis.

When you are finished, provide:

Root Cause:
Evidence:
Recommendation:
""".strip()

    print("=== AI INCIDENT INVESTIGATION LOOP ===")

    response = run_investigation_loop(
        prompt=prompt,
        max_iterations=5,
    )

    print("\n=== FINAL INCIDENT ANALYSIS ===")
    print(response.text)


if __name__ == "__main__":
    main()

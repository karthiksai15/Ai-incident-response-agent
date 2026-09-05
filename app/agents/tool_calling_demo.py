from app.agents.tool_calling import (
    ask_gemini_with_tool,
    execute_tool_call,
)


def main():

    prompt = """
Investigate incident INC-001.

You need to inspect the ERROR logs before providing
your analysis.

Use the search_logs tool to retrieve the ERROR logs
for incident INC-001.

After receiving the tool results, briefly explain:
1. What the important errors are.
2. What they suggest about the incident.
""".strip()

    print("=== GEMINI TOOL CALLING ===")

    chat, response = ask_gemini_with_tool(prompt)

    print("\nGemini initial response:")
    print(response)

    if response.function_calls:
        print("\nGemini requested a tool.")

        final_response = execute_tool_call(
            chat=chat,
            response=response,
        )

        print("\n=== FINAL GEMINI RESPONSE ===")
        print(final_response.text)

    else:
        print("\nGemini did not request a tool.")
        print(response.text)


if __name__ == "__main__":
    main()

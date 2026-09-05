from app.agents.tool_calling import (
    ask_gemini_with_tools,
    execute_tool_calls,
)


def main():

    prompt = """
You are investigating incident INC-001.

Determine whether the payment-service is currently
healthy.

Do not assume the answer from the incident logs.
Use the appropriate available tool to check the
service health.

Do not use a tool that is unrelated to this task.
""".strip()

    print("=== GEMINI TOOL SELECTION ===")

    chat, response = ask_gemini_with_tools(prompt)

    print("\nGemini response:")

    if response.function_calls:

        for function_call in response.function_calls:
            print(f"\nSelected tool: {function_call.name}")
            print(f"Arguments: {function_call.args}")

        final_response = execute_tool_calls(
            chat=chat,
            response=response,
        )

        print("\n=== FINAL RESPONSE ===")
        print(final_response.text)

    else:
        print(response.text)


if __name__ == "__main__":
    main()

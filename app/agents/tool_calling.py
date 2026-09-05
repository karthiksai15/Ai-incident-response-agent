from google.genai import types

from app.core.llm import client
from app.agents.tool_safety import validate_tool_call
from app.agents.tools import (
    execute_search_logs,
    execute_extract_errors,
    execute_check_service_health,
    execute_get_incident_context,
)


def create_tools():
    return [
        types.Tool(
            function_declarations=[
                types.FunctionDeclaration(
                    name="search_logs",
                    description=(
                        "Search logs for a specific incident. "
                        "Can filter by log level or keyword."
                    ),
                    parameters=types.Schema(
                        type=types.Type.OBJECT,
                        properties={
                            "incident_id": types.Schema(
                                type=types.Type.STRING,
                                description="Incident ID, for example INC-001.",
                            ),
                            "level": types.Schema(
                                type=types.Type.STRING,
                                description="Optional log level: INFO, WARN, or ERROR.",
                            ),
                            "keyword": types.Schema(
                                type=types.Type.STRING,
                                description="Optional keyword to search in log messages.",
                            ),
                        },
                        required=["incident_id"],
                    ),
                ),
                types.FunctionDeclaration(
                    name="extract_errors",
                    description=(
                        "Extract WARN and ERROR logs for an incident."
                    ),
                    parameters=types.Schema(
                        type=types.Type.OBJECT,
                        properties={
                            "incident_id": types.Schema(
                                type=types.Type.STRING,
                                description="Incident ID, for example INC-001.",
                            ),
                        },
                        required=["incident_id"],
                    ),
                ),
                types.FunctionDeclaration(
                    name="check_service_health",
                    description=(
                        "Check the current simulated health of a service."
                    ),
                    parameters=types.Schema(
                        type=types.Type.OBJECT,
                        properties={
                            "service": types.Schema(
                                type=types.Type.STRING,
                                description="Service name, for example payment-service.",
                            ),
                        },
                        required=["service"],
                    ),
                ),
                types.FunctionDeclaration(
                    name="get_incident_context",
                    description=(
                        "Get incident service, severity, status, and log count."
                    ),
                    parameters=types.Schema(
                        type=types.Type.OBJECT,
                        properties={
                            "incident_id": types.Schema(
                                type=types.Type.STRING,
                                description="Incident ID, for example INC-001.",
                            ),
                            "service": types.Schema(
                                type=types.Type.STRING,
                                description="Service associated with the incident.",
                            ),
                            "severity": types.Schema(
                                type=types.Type.STRING,
                                description="Incident severity.",
                            ),
                        },
                        required=[
                            "incident_id",
                            "service",
                            "severity",
                        ],
                    ),
                ),
            ]
        )
    ]


def ask_gemini_with_tools(prompt: str):
    chat = client.chats.create(
        model="gemini-3.7-flash",
        config=types.GenerateContentConfig(
            tools=create_tools(),
        ),
    )

    response = chat.send_message(prompt)

    return chat, response


def execute_tool_call(function_call):
    name = function_call.name
    args = function_call.args

    print(f"\nTool requested by Gemini: {name}")
    print(f"Tool arguments: {args}")

    # Security boundary:
    # validate the tool and its arguments
    # before executing anything.
    validate_tool_call(
        tool_name=name,
        arguments=args,
    )

    if name == "search_logs":
        result = execute_search_logs(
            incident_id=args["incident_id"],
            level=args.get("level"),
            keyword=args.get("keyword"),
        )

        result = [
            {
                "timestamp": log.timestamp.isoformat(),
                "level": log.level,
                "service": log.service,
                "message": log.message,
            }
            for log in result
        ]

    elif name == "extract_errors":
        result = execute_extract_errors(
            incident_id=args["incident_id"],
        )

        result = [
            {
                "timestamp": log.timestamp.isoformat(),
                "level": log.level,
                "service": log.service,
                "message": log.message,
            }
            for log in result
        ]

    elif name == "check_service_health":
        result = execute_check_service_health(
            service=args["service"],
        )

        result = result.model_dump()

    elif name == "get_incident_context":
        result = execute_get_incident_context(
            incident_id=args["incident_id"],
            service=args["service"],
            severity=args["severity"],
        )

        result = result.model_dump()

    else:
        result = {
            "error": f"Unknown tool: {name}"
        }

    print("Tool executed successfully.")

    return result


def run_investigation_loop(
    prompt: str,
    max_iterations: int = 5,
):
    chat, response = ask_gemini_with_tools(prompt)

    for iteration in range(max_iterations):

        print(
            f"\n--- Investigation Iteration "
            f"{iteration + 1} ---"
        )

        if not response.function_calls:
            print("Gemini produced the final response.")
            return response

        print(
            f"Gemini requested "
            f"{len(response.function_calls)} tool call(s)."
        )

        function_responses = []

        for function_call in response.function_calls:

            result = execute_tool_call(
                function_call
            )

            function_responses.append(
                types.Part.from_function_response(
                    name=function_call.name,
                    response={
                        "result": result
                    },
                )
            )

        response = chat.send_message(
            function_responses
        )

    raise RuntimeError(
        "Investigation stopped because the maximum "
        "number of iterations was reached."
    )


# Backward-compatible single-tool interface.
# Kept for existing tests and older demo code.

def create_tool():
    return types.Tool(
        function_declarations=[
            types.FunctionDeclaration(
                name="search_logs",
                description=(
                    "Search logs for a specific incident. "
                    "Can filter by log level or keyword."
                ),
                parameters=types.Schema(
                    type=types.Type.OBJECT,
                    properties={
                        "incident_id": types.Schema(
                            type=types.Type.STRING,
                            description="Incident ID, for example INC-001.",
                        ),
                        "level": types.Schema(
                            type=types.Type.STRING,
                            description="Optional log level: INFO, WARN, or ERROR.",
                        ),
                        "keyword": types.Schema(
                            type=types.Type.STRING,
                            description="Optional keyword to search in log messages.",
                        ),
                    },
                    required=["incident_id"],
                ),
            )
        ]
    )


def search_logs_tool(
    incident_id: str,
    level: str | None = None,
    keyword: str | None = None,
):
    class FunctionCall:
        def __init__(self, name, args):
            self.name = name
            self.args = args

    function_call = FunctionCall(
        name="search_logs",
        args={
            "incident_id": incident_id,
            "level": level,
            "keyword": keyword,
        },
    )

    return execute_tool_call(function_call)

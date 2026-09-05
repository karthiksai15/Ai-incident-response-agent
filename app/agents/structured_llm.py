import time

from google.genai import errors

from app.core.llm import client
from app.models.analysis import IncidentAnalysis


def analyze_with_llm(
    prompt: str,
    max_retries: int = 3,
) -> IncidentAnalysis:

    for attempt in range(max_retries):

        try:
            response = client.models.generate_content(
                model="gemini-3.7-flash",
                contents=prompt,
                config={
                    "response_mime_type": "application/json",
                    "response_schema": IncidentAnalysis,
                },
            )

            return response.parsed

        except errors.ServerError:

            if attempt == max_retries - 1:
                raise

            wait_time = 2 ** attempt
            time.sleep(wait_time)

    raise RuntimeError("LLM analysis failed.")

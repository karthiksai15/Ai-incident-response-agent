from app.core.llm import client


response = client.models.generate_content(
    model="gemini-3.7-flash",
    contents=(
        "Explain database connection pool exhaustion "
        "in one simple sentence."
    ),
)

print(response.text)

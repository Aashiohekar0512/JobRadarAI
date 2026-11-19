import os
import json

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY missing in .env")

client = genai.Client(
    api_key=API_KEY,
    http_options=types.HttpOptions(timeout=120000)
)

MODEL = "gemini-3.5-flash-lite"


def tag_job_with_llm(job):

    prompt = f"""
Classify this Indian fresher job.

Title: {job.get('title', '')}
Location: {job.get('location', '')}
Description: {str(job.get('description', ''))[:1000]}

Return only valid JSON:
{{
    "role": "short normalized job role",
    "city": "Indian city, Remote, or Unknown"
}}

Rules:
- Do not invent a city.
- Use the provided location as the primary source.
- Return Remote only if the job location is Remote.
- If the city cannot be identified, return Unknown.
"""

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )

    output = response.text

    if not output:
        raise RuntimeError("Gemini returned empty output")

    output = output.strip()

    start = output.find("{")
    end = output.rfind("}")

    if start == -1 or end == -1 or end <= start:
        raise RuntimeError(f"No JSON object found: {output!r}")

    json_text = output[start:end + 1]

    try:
        result = json.loads(json_text)
    except json.JSONDecodeError as error:
        raise RuntimeError(
            f"Invalid JSON: {json_text!r}"
        ) from error

    return {
        "role": result.get("role", "Other"),
        "city": result.get("city", "Unknown")
    }
import os
from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY or API_KEY == "PASTE_YOUR_API_KEY_HERE":
    raise ValueError("GEMINI_API_KEY is missing in .env file")

client = genai.Client(api_key=API_KEY)


class JobTags(BaseModel):
    role: str
    city: str


def tag_job_with_llm(job):
    prompt = f"""
    You are a job classification assistant.

    Read this Indian fresher job posting.

    Job Title: {job.get('title', '')}
    Company: {job.get('company', '')}
    Location: {job.get('location', '')}
    Description: {job.get('description', '')[:2000]}

    Return:
    1. role: A short normalized job role.
    2. city: The Indian city mentioned in the job location.

    Rules:
    - Do not invent a city.
    - If city is not identifiable, return Unknown.
    - If role is unclear, return Other.
    """

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": JobTags,
        },
    )

    if response.parsed:
        return response.parsed.model_dump()

    return JobTags.model_validate_json(response.text).model_dump()
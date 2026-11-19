# JobRadarAI

An AI-powered fresher jobs and internships discovery platform focused on India.

## Features
- Collects fresher job and internship listings.
- Removes duplicate job posts.
- Uses Gemini AI to classify job roles and cities.
- Provides job search and filtering.
- Stores job data in SQLite.
- Includes a manual validation sample.

## Technology Stack
- Python
- FastAPI
- SQLite
- Google Gemini API
- HTML and CSS

## Run Locally

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the application:

```bash
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000

## Environment Variables

Set `GEMINI_API_KEY` in a local `.env` file.

Do not publish API keys or secrets.

## Project Status

Prototype under development. Data quality, AI tagging accuracy, and automated refresh are being evaluated.

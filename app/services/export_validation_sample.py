import csv
import random
from pathlib import Path

from app.database import get_saved_jobs

BASE_DIR = Path(__file__).resolve().parent.parent.parent
OUTPUT_FILE = BASE_DIR / "data" / "validation_sample.csv"


def export_validation_sample():
    jobs = get_saved_jobs()

    if len(jobs) < 50:
        print("Error: At least 50 jobs are required.")
        return

    random.seed(42)
    sample_jobs = random.sample(jobs, 50)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    fields = [
        "id",
        "title",
        "company",
        "location",
        "ai_role",
        "ai_city",
        "human_role",
        "human_city",
        "role_correct",
        "city_correct"
    ]

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()

        for job in sample_jobs:
            writer.writerow({
                "id": job.get("id"),
                "title": job.get("title"),
                "company": job.get("company"),
                "location": job.get("location"),
                "ai_role": job.get("ai_role") or "",
                "ai_city": job.get("ai_city") or "",
                "human_role": "",
                "human_city": "",
                "role_correct": "",
                "city_correct": ""
            })

    print("Validation sample created:", OUTPUT_FILE)
    print("Total jobs exported:", len(sample_jobs))


if __name__ == "__main__":
    export_validation_sample()
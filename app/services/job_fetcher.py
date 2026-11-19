import requests
from app.database import save_jobs

API_URL = "https://jobsforceindia.com/api/public/v1/jobs"

HEADERS = {
    "Accept": "application/json",
    "User-Agent": "JobRadarAI/1.0"
}


def get_monthly_salary(salary):
    if not salary:
        return None

    minimum = salary.get("min")
    period = salary.get("period")

    if minimum is None:
        return None

    if period == "monthly":
        return int(minimum)

    if period == "yearly":
        return int(minimum / 12)

    return None


def fetch_jobs():
    collected_jobs = []
    seen_ids = set()

    for page in range(1, 11):
        params = {
            "fresher": "true",
            "page": page,
            "per_page": 20
        }

        try:
            response = requests.get(
                API_URL,
                params=params,
                headers=HEADERS,
                timeout=30
            )

            if response.status_code == 429:
                print("API rate limit reached. Try later.")
                break

            response.raise_for_status()
            data = response.json()

            results = data.get("results", [])

            if not results:
                break

            for item in results:
                job_id = str(item.get("id", ""))

                if not job_id or job_id in seen_ids:
                    continue

                seen_ids.add(job_id)

                hiring = item.get("hiring") or {}
                location_data = item.get("location") or {}
                experience_data = item.get("experience") or {}
                salary_data = item.get("salary") or {}

                city = location_data.get("city") or ""
                state = location_data.get("state") or ""

                location = ", ".join(
                    part for part in [city, state] if part
                )

                if location_data.get("remote"):
                    location = "Remote"

                collected_jobs.append({
                    "id": job_id,
                    "title": item.get("title", "Not specified"),
                    "company": hiring.get(
                        "display", "Not specified"
                    ),
                    "location": location or "Not specified",
                    "category": item.get(
                        "category", "Uncategorized"
                    ),
                    "job_type": item.get(
                        "job_type", "Not specified"
                    ),
                    "experience": experience_data.get(
                        "label", "Fresher - To Verify"
                    ),
                    "salary": get_monthly_salary(salary_data),
                    "description": item.get("summary", ""),
                    "source_url": item.get("url", ""),
                    "apply_url": item.get("apply_url", ""),
                    "source": "JobsForce India",
                    "posted_date": item.get("posted_date")
                })

            next_page = data.get("next_page")

            if not next_page:
                break

        except requests.RequestException as error:
            print("Job API connection error:", error)
            break

        except ValueError as error:
            print("Invalid API response:", error)
            break

    return collected_jobs


if __name__ == "__main__":
    jobs = fetch_jobs()
    saved_count = save_jobs(jobs)
    print("New jobs saved in database:", saved_count)

    print("\nJobRadarAI - Live Job Fetcher")
    print("Total fresher jobs collected:", len(jobs))

    for job in jobs[:10]:
        print("\nTitle:", job["title"])
        print("Company:", job["company"])
        print("Location:", job["location"])
        print("Apply:", job["apply_url"])
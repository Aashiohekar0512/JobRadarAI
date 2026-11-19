import time

from app.database import get_saved_jobs, get_connection
from app.services.llm_tagger import tag_job_with_llm


def process_all_jobs(limit=20):

    # Only select jobs that have not been processed
    jobs = [
        job for job in get_saved_jobs()
        if not job["ai_processed"]
    ]

    print("Pending jobs found:", len(jobs))

    if limit:
        jobs = jobs[:limit]

    print("Jobs selected for LLM tagging:", len(jobs))

    conn = get_connection()
    updated_count = 0
    failed_count = 0

    try:
        for index, job in enumerate(jobs):

            job_id = job["id"]

            print("\nProcessing Job ID:", job_id)
            print("Title:", job["title"])

            success = False

            # Retry up to 3 attempts
            for attempt in range(1, 4):

                try:
                    result = tag_job_with_llm(job)

                    conn.execute(
                        """
                        UPDATE jobs
                        SET ai_role = ?,
                            ai_city = ?,
                            ai_processed = 1
                        WHERE id = ?
                        """,
                        (
                            result["role"],
                            result["city"],
                            job_id
                        )
                    )

                    conn.commit()
                    updated_count += 1
                    success = True

                    print("Role:", result["role"])
                    print("City:", result["city"])
                    print("Status: Saved successfully")

                    break

                except Exception as error:

                    error_message = str(error)

                    if (
                        "429" in error_message
                        or "RESOURCE_EXHAUSTED" in error_message
                    ) and attempt < 3:

                        print(
                            f"Rate limit reached. "
                            f"Waiting 45 seconds. "
                            f"Retry {attempt}/2"
                        )

                        time.sleep(45)

                    else:
                        print("Tagging failed:", error)
                        break

            if not success:
                failed_count += 1

            # Keep requests below the Free Tier RPM limit
            if index < len(jobs) - 1:
                time.sleep(5)

    finally:
        conn.close()

    print("\n========== LLM TAGGING REPORT ==========")
    print("Updated Jobs:", updated_count)
    print("Failed Jobs:", failed_count)
    print("========================================")


if __name__ == "__main__":
    process_all_jobs(limit=50)
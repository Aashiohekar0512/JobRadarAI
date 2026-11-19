from app.database import get_saved_jobs


def clean_jobs():
    jobs = get_saved_jobs()

    seen_urls = set()
    cleaned_jobs = []
    duplicate_jobs = []
    invalid_count = 0
    missing_apply_link = 0
    missing_source_url = 0

    for job in jobs:
        title = (job["title"] or "").strip()
        company = (job["company"] or "").strip()
        source_url = (job["source_url"] or "").strip()

        # Check required information
        if not title or not company:
            invalid_count += 1
            continue

        # Check duplicate using source URL
        if source_url:
            if source_url in seen_urls:
                duplicate_jobs.append(job)
                continue

            seen_urls.add(source_url)
        else:
            missing_source_url += 1

        cleaned_jobs.append(job)

        # Check application link
        apply_url = (job["apply_url"] or "").strip()

        if not apply_url.startswith("https://"):
            missing_apply_link += 1

    print("JobRadarAI - Job Data Quality Report")
    print("------------------------------------")
    print(f"Total Jobs: {len(jobs)}")
    print(f"Valid Jobs: {len(cleaned_jobs)}")
    print(f"Duplicate Jobs: {len(duplicate_jobs)}")
    print(f"Invalid Jobs: {invalid_count}")
    print(f"Missing Source URL: {missing_source_url}")
    print(f"Jobs Without Apply Link: {missing_apply_link}")

    print("\nDuplicate Jobs List:")
    print("--------------------")

    for job in duplicate_jobs:
        print(
            f"ID: {job['id']} | "
            f"Title: {job['title']} | "
            f"Company: {job['company']}"
        )

    return cleaned_jobs


if __name__ == "__main__":
    clean_jobs()
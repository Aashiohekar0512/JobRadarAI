from apscheduler.schedulers.background import BackgroundScheduler
from app.services.job_fetcher import fetch_jobs
from app.database import save_jobs


def refresh_jobs():
    print("Job Refresh Started...")

    try:
        jobs = fetch_jobs()

        if jobs:
            saved_count = save_jobs(jobs)
            print("Jobs collected:", len(jobs))
            print("New jobs saved:", saved_count)
        else:
            print("No jobs fetched.")

    except Exception as error:
        print("Job refresh failed:", error)

    print("Job Refresh Completed.")


scheduler = BackgroundScheduler()


def start_scheduler():
    if not scheduler.running:

        # Run once immediately after deployment
        scheduler.add_job(
            refresh_jobs,
            trigger="date",
            id="initial_job_refresh",
            replace_existing=True
        )

        # Then refresh every 24 hours
        scheduler.add_job(
            refresh_jobs,
            trigger="interval",
            hours=24,
            id="daily_job_refresh",
            replace_existing=True
        )

        scheduler.start()
        print("Daily Job Scheduler Started.")


if __name__ == "__main__":
    start_scheduler()
from apscheduler.schedulers.background import BackgroundScheduler
from app.services.job_fetcher import fetch_jobs
from app.database import save_jobs


def refresh_jobs():
    print("Daily Job Refresh Started...")

    jobs = fetch_jobs()

    if jobs:
        save_jobs(jobs)
        print("New jobs fetched:", len(jobs))
    else:
        print("No new jobs found.")

    print("Daily Job Refresh Completed.")


scheduler = BackgroundScheduler()


def start_scheduler():
    if not scheduler.running:
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
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

DB_PATH = DATA_DIR / "jobs.db"


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                company TEXT NOT NULL,
                location TEXT,
                category TEXT,
                job_type TEXT,
                experience TEXT,
                salary INTEGER,
                description TEXT,
                source_url TEXT,
                apply_url TEXT,
                source TEXT,
                posted_date TEXT
            )
        """)

        columns = {
            row["name"]
            for row in connection.execute(
                "PRAGMA table_info(jobs)"
            ).fetchall()
        }

        new_columns = {
    "source_url": "TEXT",
    "apply_url": "TEXT",
    "source": "TEXT",
    "posted_date": "TEXT",
    "ai_category": "TEXT",
"ai_skills": "TEXT",
"ai_processed": "INTEGER DEFAULT 0",
"ai_role": "TEXT",
"ai_city": "TEXT"
}

        for name, data_type in new_columns.items():
            if name not in columns:
                connection.execute(
                    f"ALTER TABLE jobs ADD COLUMN {name} {data_type}"
                )

        connection.execute("""
            CREATE UNIQUE INDEX IF NOT EXISTS unique_job_source_url
            ON jobs(source_url)
            WHERE source_url IS NOT NULL AND source_url != ''
        """)


def save_jobs(jobs):
    init_db()
    inserted_count = 0

    with get_connection() as connection:
        for job in jobs:
            cursor = connection.execute("""
                INSERT OR IGNORE INTO jobs (
                    title, company, location, category,
                    job_type, experience, salary, description,
                    source_url, apply_url, source, posted_date
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                job.get("title", "Not specified"),
                job.get("company", "Not specified"),
                job.get("location", "Not specified"),
                job.get("category", "Uncategorized"),
                job.get("job_type", "Not specified"),
                job.get("experience", "Not specified"),
                job.get("salary"),
                job.get("description", ""),
                job.get("source_url"),
                job.get("apply_url"),
                job.get("source", "Unknown"),
                job.get("posted_date")
            ))

            inserted_count += cursor.rowcount

    return inserted_count


def get_saved_jobs():
    init_db()

    with get_connection() as connection:
        rows = connection.execute(
            "SELECT * FROM jobs ORDER BY id DESC"
        ).fetchall()

    return [dict(row) for row in rows]

def update_ai_tags(job_id, ai_category, ai_skills, ai_role=None, ai_city=None):
    import json

    with get_connection() as connection:
        connection.execute("""
            UPDATE jobs
            SET ai_category = ?,
                ai_skills = ?,
                ai_role = ?,
                ai_city = ?,
                ai_processed = 1
            WHERE id = ?
        """, (
            ai_category,
            json.dumps(ai_skills),
            ai_role,
            ai_city,
            job_id
        ))

if __name__ == "__main__":
    init_db()
    print("JobRadarAI Database Ready!")
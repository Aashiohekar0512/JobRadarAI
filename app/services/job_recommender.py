import json

from app.database import get_saved_jobs


def recommend_jobs(user_skills):
    jobs = get_saved_jobs()

    user_skills = [
        skill.strip().lower()
        for skill in user_skills.split(",")
        if skill.strip()
    ]

    recommendations = []

    for job in jobs:
        job_skills = json.loads(job.get("ai_skills") or "[]")

        matched_skills = [
            skill for skill in user_skills
            if skill in [s.lower() for s in job_skills]
        ]

        if matched_skills:
            score = round(
                len(matched_skills) / len(user_skills) * 100
            )

            recommendations.append({
                "title": job["title"],
                "company": job["company"],
                "location": job["location"],
                "matched_skills": matched_skills,
                "match_score": score,
                "apply_url": job["apply_url"]
            })

    recommendations.sort(
        key=lambda job: job["match_score"],
        reverse=True
    )

    return recommendations


if __name__ == "__main__":
    skills = input("Enter your skills (Python, SQL, Excel): ")

    results = recommend_jobs(skills)

    print("\nRecommended Jobs:", len(results))

    for job in results[:10]:
        print("\nJob:", job["title"])
        print("Company:", job["company"])
        print("Location:", job["location"])
        print("Matched Skills:", job["matched_skills"])
        print("Match Score:", str(job["match_score"]) + "%")
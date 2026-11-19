def tag_job(job):
    title = (job.get("title") or "").lower()
    description = (job.get("description") or "").lower()

    text = title + " " + description

    categories = {
        "IT": [
            "python", "java", "developer", "software",
            "data analyst", "programming", "data analysis",
            "software tester", "html", "javascript"
        ],
        "Marketing": [
            "marketing", "seo", "social media",
            "content writer", "digital content"
        ],
        "Finance": [
            "finance", "accounting", "banking",
            "financial analyst", "financial data"
        ],
        "Sales": [
            "sales", "business development",
            "sales executive", "retail sales"
        ],
        "Customer Support": [
            "customer support", "customer service",
            "customer experience", "customer satisfaction",
            "call center"
        ],
        "Data Entry": [
            "data entry", "data management",
            "typing", "data processing"
        ]
    }

    skills = [
        "python", "java", "excel", "sql",
        "communication", "marketing", "html",
        "css", "javascript", "data analysis",
        "data entry", "data management",
        "financial analyst", "financial data",
        "financial analysis", "analyzing financial data",
        "preparing reports", "reports",
        "customer service", "customer support",
        "customer satisfaction", "support services",
        "customer experience",
        "content writing", "seo", "social media",
        "programming", "typing",
        "software development", "software testing"
    ]

    detected_category = "Other"

    for category, keywords in categories.items():
        if any(word in text for word in keywords):
            detected_category = category
            break

    detected_skills = [
        skill for skill in skills if skill in text
    ]

    job["ai_category"] = detected_category
    job["ai_skills"] = detected_skills

    return job


def tag_jobs(jobs):
    return [tag_job(job) for job in jobs]
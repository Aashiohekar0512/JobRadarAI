from fastapi import APIRouter, Query
from typing import Optional

from app.database import get_saved_jobs
from fastapi import Request
from fastapi.templating import Jinja2Templates

jobs_router = APIRouter(
    prefix="/jobs",
    tags=["Job Search"]
)
templates = Jinja2Templates(directory="app/templates")

@jobs_router.get("/")
def get_all_jobs(request: Request):
    jobs = get_saved_jobs()

    return templates.TemplateResponse(
        request=request,
        name="jobs.html",
        context={
            "jobs": jobs,
            "total_jobs": len(jobs),
            "keyword": "",
            "location": "",
            "category": "",
            "job_type": ""
        }
    )

@jobs_router.get("/search")
def search_jobs(
    keyword: Optional[str] = Query(None),
    location: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    job_type: Optional[str] = Query(None),
    min_salary: Optional[int] = Query(None),
    max_salary: Optional[int] = Query(None)
):
    results = get_saved_jobs()

    if keyword:
        results = [
            job for job in results
            if keyword.lower() in (job["title"] or "").lower()
            or keyword.lower() in (job["description"] or "").lower()
        ]

    if location:
        results = [
            job for job in results
            if location.lower() in (job["location"] or "").lower()
        ]

    if category:
        results = [
            job for job in results
            if category.lower() in (job["category"] or "").lower()
        ]

    if job_type:
        results = [
            job for job in results
            if job["job_type"]
            and job["job_type"].lower() == job_type.lower()
        ]

    if min_salary is not None:
        results = [
            job for job in results
            if job["salary"] is not None
            and job["salary"] >= min_salary
        ]

    if max_salary is not None:
        results = [
            job for job in results
            if job["salary"] is not None
            and job["salary"] <= max_salary
        ]

    return {
        "status": "success",
        "total_jobs": len(results),
        "jobs": results
    }


@jobs_router.get("/categories")
def get_categories():
    jobs = get_saved_jobs()

    categories = sorted({
        job["category"]
        for job in jobs
        if job["category"]
    })

    return {
        "status": "success",
        "categories": categories
    }


@jobs_router.get("/{job_id}")
def get_job_details(job_id: int):
    jobs = get_saved_jobs()

    for job in jobs:
        if job["id"] == job_id:
            return {
                "status": "success",
                "job": job
            }

    return {
        "status": "error",
        "message": "Job not found"
    }

@jobs_router.get("/view/{job_id}")
def view_job_details(request: Request, job_id: int):
    jobs = get_saved_jobs()

    for job in jobs:
        if job["id"] == job_id:
            return templates.TemplateResponse(
                request=request,
                name="job_details.html",
                context={"job": job}
            )

    return templates.TemplateResponse(
        request=request,
        name="job_details.html",
        context={
            "job": {
                "title": "Job Not Found",
                "company": None,
                "location": None,
                "category": None,
                "ai_category": None,
                "job_type": None,
                "experience": None,
                "salary": None,
                "posted_date": None,
                "description": "This job could not be found.",
                "apply_url": None
            }
        },
        status_code=404
    )
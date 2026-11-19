from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

from app.jobs import jobs_router
from app.database import get_saved_jobs
from app.recommend import recommend_router
from app.services.scheduler import start_scheduler, scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    start_scheduler()
    yield

    if scheduler.running:
        scheduler.shutdown(wait=False)


app = FastAPI(
    title="JobRadarAI",
    description="AI Powered Fresher Job Search Platform - All India",
    version="1.0.0",
    lifespan=lifespan
)

templates = Jinja2Templates(directory="app/templates")

app.include_router(jobs_router)
app.include_router(recommend_router)


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


@app.get("/search")
def search_page(
    request: Request,
    keyword: str = "",
    location: str = "",
    category: str = "",
    job_type: str = ""
):
    jobs = get_saved_jobs()

    if keyword:
        jobs = [
            job for job in jobs
            if keyword.lower() in (job["title"] or "").lower()
            or keyword.lower() in (job["description"] or "").lower()
        ]

    if location:
        jobs = [
            job for job in jobs
            if location.lower() in (job["location"] or "").lower()
        ]

    if category:
        jobs = [
            job for job in jobs
            if category.lower() == (job["category"] or "").lower()
        ]

    if job_type:
        jobs = [
            job for job in jobs
            if job_type.lower() == (job["job_type"] or "").lower()
        ]

    return templates.TemplateResponse(
        request=request,
        name="jobs.html",
        context={
            "jobs": jobs,
            "total_jobs": len(jobs),
            "keyword": keyword,
            "location": location,
            "category": category,
            "job_type": job_type
        }
    )


@app.get("/health")
def health():
    return {
        "status": "success",
        "application": "JobRadarAI"
    }
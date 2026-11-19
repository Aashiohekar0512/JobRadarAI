from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from app.services.job_recommender import recommend_jobs

recommend_router = APIRouter()

templates = Jinja2Templates(directory="app/templates")


@recommend_router.get("/recommend")
def recommend_page(request: Request, skills: str = ""):
    recommendations = []

    if skills.strip():
        recommendations = recommend_jobs(skills)

    return templates.TemplateResponse(
        request=request,
        name="recommend.html",
        context={
            "skills": skills,
            "recommendations": recommendations,
            "total_jobs": len(recommendations)
        }
    )
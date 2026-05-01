from __future__ import annotations

from fastapi import FastAPI, File, Form, HTTPException, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from analyzer.gap import find_weak_sections
from analyzer.matcher import match_skills
from analyzer.scorer import calculate_score
from analyzer.skills import extract_skills, infer_required_skills
from ai_engine.feedback import generate_feedback
from config import settings
from parser.resume_parser import UnsupportedResumeFormat, parse_resume
from schemas import AnalyzeResponse, HealthResponse


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    docs_url="/docs" if settings.environment != "production" else None,
    redoc_url="/redoc" if settings.environment != "production" else None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"message": exc.detail, "status_code": exc.status_code}},
    )


@app.get("/health", response_model=HealthResponse)
def health() -> dict:
    return {
        "status": "ok",
        "version": settings.app_version,
        "environment": settings.environment,
    }


@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_resume(
    resume: UploadFile = File(...),
    job_role: str = Form(""),
) -> dict:
    if not resume.filename:
        raise HTTPException(status_code=400, detail="Resume filename is required.")

    if resume.size is not None and resume.size > settings.max_upload_bytes:
        raise HTTPException(status_code=413, detail="Resume file is too large.")

    try:
        content = await resume.read()
        if len(content) > settings.max_upload_bytes:
            raise HTTPException(status_code=413, detail="Resume file is too large.")
        resume_text = parse_resume(resume.filename or "resume.txt", content)
    except UnsupportedResumeFormat as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=400, detail="Could not parse resume file.") from exc

    if not resume_text:
        raise HTTPException(status_code=400, detail="Resume text is empty.")

    resume_skills = extract_skills(resume_text)
    required_skills = infer_required_skills(job_role)
    match = match_skills(resume_skills, required_skills)
    weak_sections = find_weak_sections(resume_text)
    score = calculate_score(
        resume_text=resume_text,
        skill_match_score=match["skill_match_score"],
        weak_sections=weak_sections,
    )
    feedback = generate_feedback(
        resume_text=resume_text,
        job_role=job_role,
        matched_skills=match["matched_skills"],
        missing_skills=match["missing_skills"],
        weak_sections=weak_sections,
    )

    return {
        "filename": resume.filename,
        "job_role": job_role.strip(),
        "resume_preview": resume_text[: settings.resume_preview_chars],
        "resume_skills": resume_skills,
        "required_skills": required_skills,
        "matched_skills": match["matched_skills"],
        "missing_skills": match["missing_skills"],
        "weak_sections": weak_sections,
        "score": score,
        "feedback": feedback,
    }

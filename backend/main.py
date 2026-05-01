from __future__ import annotations

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from analyzer.gap import find_weak_sections
from analyzer.matcher import match_skills
from analyzer.scorer import calculate_score
from analyzer.skills import extract_skills, infer_required_skills
from ai_engine.feedback import generate_feedback
from parser.resume_parser import UnsupportedResumeFormat, parse_resume


app = FastAPI(title="AI Resume Analyzer", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/analyze")
async def analyze_resume(
    resume: UploadFile = File(...),
    job_role: str = Form(""),
) -> dict:
    try:
        content = await resume.read()
        resume_text = parse_resume(resume.filename or "resume.txt", content)
    except UnsupportedResumeFormat as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
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
        job_role=job_role,
        matched_skills=match["matched_skills"],
        missing_skills=match["missing_skills"],
        weak_sections=weak_sections,
    )

    return {
        "filename": resume.filename,
        "job_role": job_role,
        "resume_preview": resume_text[:800],
        "resume_skills": resume_skills,
        "required_skills": required_skills,
        "matched_skills": match["matched_skills"],
        "missing_skills": match["missing_skills"],
        "weak_sections": weak_sections,
        "score": score,
        "feedback": feedback,
    }


from __future__ import annotations

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str
    version: str
    environment: str


class ScoreBreakdown(BaseModel):
    skills: int = Field(ge=0, le=100)
    experience: int = Field(ge=0, le=100)
    projects: int = Field(ge=0, le=100)
    ats_format: int = Field(ge=0, le=100)


class Score(BaseModel):
    overall: int = Field(ge=0, le=100)
    breakdown: ScoreBreakdown


class Feedback(BaseModel):
    strengths: list[str]
    weaknesses: list[str]
    improvements: list[str]
    rewritten_bullets: list[str]


class AnalyzeResponse(BaseModel):
    filename: str | None
    job_role: str
    resume_preview: str
    resume_skills: list[str]
    required_skills: list[str]
    matched_skills: list[str]
    missing_skills: list[str]
    weak_sections: list[str]
    score: Score
    feedback: Feedback

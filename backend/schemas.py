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
    source: str
    role_type: str | None = None
    strengths: list[str]
    weaknesses: list[str]
    improvements: list[str]
    priority_actions: list[str]
    rewritten_bullets: list[str]
    interview_questions: list[str]


class ATSCompliance(BaseModel):
    score: int = Field(ge=0, le=100)
    issues: list[str]
    recommendations: list[str]


class SkillRoadmap(BaseModel):
    skill: str
    difficulty: str
    estimated_weeks: int
    resources: list[str]
    certifications: list[str]
    priority: str


class UpskillRoadmap(BaseModel):
    total_weeks: int
    priority_order: list[str]
    skills_roadmap: list[SkillRoadmap]
    message: str


class AnalyzeResponse(BaseModel):
    filename: str | None
    job_role: str
    resume_skills: list[str]
    required_skills: list[str]
    matched_skills: list[str]
    missing_skills: list[str]
    weak_sections: list[str]
    score: Score
    feedback: Feedback
    ats_compliance: ATSCompliance
    upskilling_roadmap: UpskillRoadmap

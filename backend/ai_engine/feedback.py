from __future__ import annotations

import json
from typing import Any

from config import settings


def generate_feedback(
    *,
    resume_text: str,
    job_role: str,
    matched_skills: list[str],
    missing_skills: list[str],
    weak_sections: list[str],
) -> dict:
    if settings.openai_api_key:
        ai_feedback = _generate_openai_feedback(
            resume_text=resume_text,
            job_role=job_role,
            matched_skills=matched_skills,
            missing_skills=missing_skills,
            weak_sections=weak_sections,
        )
        if ai_feedback:
            return ai_feedback

    return _generate_fallback_feedback(
        job_role=job_role,
        matched_skills=matched_skills,
        missing_skills=missing_skills,
        weak_sections=weak_sections,
    )


def _generate_fallback_feedback(
    *,
    job_role: str,
    matched_skills: list[str],
    missing_skills: list[str],
    weak_sections: list[str],
) -> dict:
    strengths = []
    if matched_skills:
        strengths.append(
            "Your resume already shows relevant skills: "
            + ", ".join(matched_skills[:8])
            + "."
        )
    else:
        strengths.append(
            "The resume has a starting structure that can be shaped toward the target role."
        )

    weaknesses = []
    if missing_skills:
        weaknesses.append(
            "Add evidence for missing role skills: " + ", ".join(missing_skills[:8]) + "."
        )
    if weak_sections:
        weaknesses.append("Strengthen these sections: " + ", ".join(weak_sections) + ".")

    improvements = [
        f"Tailor the summary and top skills to the {job_role or 'target'} role.",
        "Convert responsibilities into impact bullets with metrics, tools, and outcomes.",
        "Place the most relevant projects and experience near the top of the resume.",
    ]

    priority_actions = [
        "Add the most important missing skills near the top of the resume with proof through projects or experience.",
        "Rewrite the weakest experience bullets with measurable impact, tools used, and business outcomes.",
        "Improve ATS clarity by using standard section headings and role-relevant keywords.",
    ]

    rewritten_bullets = [
        "Built and improved a project using relevant tools, reducing manual effort and improving user workflow.",
        "Collaborated with teammates to deliver features, debug issues, and document technical decisions.",
    ]

    interview_questions = [
        f"How does your recent work prepare you for the {job_role or 'target'} role?",
        "Which project best demonstrates your technical depth, and what measurable result did it achieve?",
        "What tradeoffs did you make while delivering a feature under constraints?",
    ]

    return {
        "source": "fallback",
        "strengths": strengths,
        "weaknesses": weaknesses
        or ["No major weaknesses detected in the current MVP analysis."],
        "improvements": improvements,
        "priority_actions": priority_actions,
        "rewritten_bullets": rewritten_bullets,
        "interview_questions": interview_questions,
    }


def _generate_openai_feedback(
    *,
    resume_text: str,
    job_role: str,
    matched_skills: list[str],
    missing_skills: list[str],
    weak_sections: list[str],
) -> dict | None:
    try:
        from openai import OpenAI
    except ImportError:
        return None

    client = OpenAI(api_key=settings.openai_api_key, timeout=settings.openai_timeout_seconds)
    prompt = _build_prompt(
        resume_text=resume_text,
        job_role=job_role,
        matched_skills=matched_skills,
        missing_skills=missing_skills,
        weak_sections=weak_sections,
    )

    schema = {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "strengths": {"type": "array", "items": {"type": "string"}},
            "weaknesses": {"type": "array", "items": {"type": "string"}},
            "improvements": {"type": "array", "items": {"type": "string"}},
            "priority_actions": {"type": "array", "items": {"type": "string"}},
            "rewritten_bullets": {"type": "array", "items": {"type": "string"}},
            "interview_questions": {"type": "array", "items": {"type": "string"}},
        },
        "required": [
            "strengths",
            "weaknesses",
            "improvements",
            "priority_actions",
            "rewritten_bullets",
            "interview_questions",
        ],
    }

    try:
        response = client.responses.create(
            model=settings.openai_model,
            instructions=(
                "You are an expert recruiter and resume coach. "
                "Return practical, concise, role-specific advice. "
                "Do not use markdown. Keep each list item to one sentence."
            ),
            input=prompt,
            text={
                "format": {
                    "type": "json_schema",
                    "name": "resume_feedback",
                    "strict": True,
                    "schema": schema,
                }
            },
        )
    except Exception:
        return None

    output_text = getattr(response, "output_text", "") or ""
    if not output_text:
        return None

    try:
        parsed = json.loads(output_text)
    except json.JSONDecodeError:
        return None

    return {
        "source": "openai",
        "strengths": _normalize_list(parsed.get("strengths"), fallback_count=2),
        "weaknesses": _normalize_list(parsed.get("weaknesses"), fallback_count=2),
        "improvements": _normalize_list(parsed.get("improvements"), fallback_count=3),
        "priority_actions": _normalize_list(parsed.get("priority_actions"), fallback_count=3),
        "rewritten_bullets": _normalize_list(parsed.get("rewritten_bullets"), fallback_count=3),
        "interview_questions": _normalize_list(parsed.get("interview_questions"), fallback_count=3),
    }


def _build_prompt(
    *,
    resume_text: str,
    job_role: str,
    matched_skills: list[str],
    missing_skills: list[str],
    weak_sections: list[str],
) -> str:
    return (
        f"Target role or job description:\n{job_role or 'Not provided'}\n\n"
        f"Matched skills:\n{', '.join(matched_skills) or 'None'}\n\n"
        f"Missing skills:\n{', '.join(missing_skills) or 'None'}\n\n"
        f"Weak sections:\n{', '.join(weak_sections) or 'None'}\n\n"
        "Resume text:\n"
        f"{resume_text[:8000]}"
    )


def _normalize_list(value: Any, *, fallback_count: int) -> list[str]:
    if not isinstance(value, list):
        return []
    normalized = [str(item).strip() for item in value if str(item).strip()]
    return normalized[:fallback_count]

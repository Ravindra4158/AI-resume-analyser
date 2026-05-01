from __future__ import annotations

import re


def calculate_score(
    resume_text: str,
    skill_match_score: int,
    weak_sections: list[str],
) -> dict:
    experience_score = _section_score("experience", weak_sections)
    projects_score = _section_score("projects", weak_sections)
    ats_score = _ats_score(resume_text)

    final_score = round(
        (skill_match_score * 0.4)
        + (experience_score * 0.3)
        + (projects_score * 0.2)
        + (ats_score * 0.1)
    )

    return {
        "overall": final_score,
        "breakdown": {
            "skills": skill_match_score,
            "experience": experience_score,
            "projects": projects_score,
            "ats_format": ats_score,
        },
    }


def _section_score(section: str, weak_sections: list[str]) -> int:
    return 45 if section in weak_sections else 85


def _ats_score(resume_text: str) -> int:
    has_email = bool(re.search(r"[\w.-]+@[\w.-]+\.\w+", resume_text))
    has_phone = bool(re.search(r"(\+?\d[\d\s().-]{8,}\d)", resume_text))
    has_common_headings = any(
        heading in resume_text.lower()
        for heading in ["skills", "experience", "projects", "education"]
    )

    return (30 if has_email else 0) + (30 if has_phone else 0) + (40 if has_common_headings else 0)


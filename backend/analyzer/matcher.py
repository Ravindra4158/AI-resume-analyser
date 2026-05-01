from __future__ import annotations


def match_skills(resume_skills: list[str], required_skills: list[str]) -> dict:
    resume_set = set(resume_skills)
    required_set = set(required_skills)

    matched = sorted(resume_set & required_set)
    missing = sorted(required_set - resume_set)
    score = round((len(matched) / len(required_set)) * 100) if required_set else 0

    return {
        "matched_skills": matched,
        "missing_skills": missing,
        "skill_match_score": score,
    }


from __future__ import annotations

import json
import re
from functools import lru_cache
from pathlib import Path


DATA_PATH = Path(__file__).resolve().parents[2] / "data" / "skills_db.json"


@lru_cache(maxsize=1)
def load_skills() -> list[str]:
    with DATA_PATH.open("r", encoding="utf-8") as file:
        skills = json.load(file)
    return sorted({skill.lower() for skill in skills})


def extract_skills(text: str) -> list[str]:
    normalized = text.lower()
    found: list[str] = []

    for skill in load_skills():
        pattern = r"(?<![\w.+#-])" + re.escape(skill) + r"(?![\w.+#-])"
        if re.search(pattern, normalized):
            found.append(skill)

    return found


def infer_required_skills(job_text: str) -> list[str]:
    skills = extract_skills(job_text)
    if skills:
        return skills

    role_defaults = {
        "frontend": ["react", "javascript", "typescript", "html", "css"],
        "backend": ["python", "fastapi", "sql", "postgresql", "docker"],
        "full stack": ["react", "python", "sql", "api", "javascript"],
        "data scientist": ["python", "machine learning", "sql", "pandas", "statistics"],
        "ml engineer": ["python", "machine learning", "docker", "api", "tensorflow"],
    }

    normalized = job_text.lower()
    for role, defaults in role_defaults.items():
        if role in normalized:
            return defaults

    return ["python", "sql", "communication", "problem solving"]


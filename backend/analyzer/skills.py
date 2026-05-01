from __future__ import annotations

import json
import re
from functools import lru_cache
from pathlib import Path


DATA_PATH = Path(__file__).resolve().parents[2] / "data" / "skills_db.json"
ROLE_DATA_PATH = Path(__file__).resolve().parents[2] / "data" / "job_roles.json"


@lru_cache(maxsize=1)
def load_skills() -> list[str]:
    with DATA_PATH.open("r", encoding="utf-8") as file:
        skills = json.load(file)
    return sorted({skill.lower() for skill in skills})


@lru_cache(maxsize=1)
def load_job_roles() -> list[dict[str, list[str] | str]]:
    with ROLE_DATA_PATH.open("r", encoding="utf-8") as file:
        roles = json.load(file)

    normalized_roles: list[dict[str, list[str] | str]] = []
    for role in roles:
        normalized_roles.append(
            {
                "name": str(role["name"]).lower(),
                "keywords": sorted({str(keyword).lower() for keyword in role["keywords"] if str(keyword).strip()}),
                "skills": sorted({str(skill).lower() for skill in role["skills"] if str(skill).strip()}),
            }
        )

    return normalized_roles


def extract_skills(text: str) -> list[str]:
    normalized = text.lower()
    found: list[str] = []

    for skill in load_skills():
        pattern = r"(?<![\w])" + re.escape(skill) + r"(?![\w])"
        if re.search(pattern, normalized):
            found.append(skill)

    return found


def _keyword_hits(text: str, keywords: list[str]) -> int:
    hits = 0
    for keyword in keywords:
        pattern = r"(?<![\w])" + re.escape(keyword) + r"(?![\w])"
        if re.search(pattern, text):
            hits += 1
    return hits


def _unique(items: list[str]) -> list[str]:
    return list(dict.fromkeys(item for item in items if item))


def infer_required_skills(job_text: str) -> list[str]:
    normalized = job_text.lower()
    exact_skills = extract_skills(job_text)

    role_hits: list[tuple[int, dict[str, list[str] | str]]] = []
    for role in load_job_roles():
        score = _keyword_hits(normalized, role["keywords"])
        if score:
            role_hits.append((score, role))

    role_hits.sort(key=lambda item: (item[0], len(item[1]["skills"])), reverse=True)

    required_skills: list[str] = []
    required_skills.extend(exact_skills)

    if role_hits:
        top_score = role_hits[0][0]
        for score, role in role_hits[:3]:
            if score >= max(1, top_score - 1):
                required_skills.extend(role["skills"])
    elif not required_skills:
        role_defaults = {
            # Tech roles
            "frontend": ["react", "javascript", "typescript", "html", "css", "tailwind", "api", "git"],
            "backend": ["python", "fastapi", "sql", "postgresql", "docker", "api", "git"],
            "full stack": ["react", "python", "sql", "api", "javascript", "docker", "git"],
            "data scientist": ["python", "machine learning", "sql", "pandas", "statistics", "tensorflow"],
            "ml engineer": ["python", "machine learning", "docker", "api", "tensorflow", "aws", "kubernetes"],
            "devops": ["docker", "kubernetes", "aws", "linux", "terraform", "ci/cd", "git"],
            "cloud": ["aws", "azure", "gcp", "docker", "kubernetes", "infrastructure as code"],
            "data engineer": ["python", "sql", "spark", "airflow", "databases", "etl"],
            "mobile": ["react native", "flutter", "java", "kotlin", "swift"],
            "software engineer": ["java", "c++", "python", "git", "problem solving", "software design"],
            "network": ["networking", "cisco", "network troubleshooting", "network protocols", "linux"],
            "database": ["sql", "postgresql", "database tuning", "backup and recovery"],
            "cybersecurity": ["cybersecurity", "network security", "ethical hacking", "owasp", "penetration testing"],
            # MBA roles
            "business analyst": ["communication", "problem solving", "excel", "sql", "presentation", "data analysis"],
            "management consultant": ["communication", "problem solving", "presentation", "excel", "project management", "strategic thinking"],
            "project manager": ["communication", "leadership", "agile", "jira", "excel", "problem solving"],
            "business development": ["communication", "negotiation", "presentation", "crm", "excel", "lead generation"],
            "strategy": ["communication", "data analysis", "excel", "presentation", "strategic thinking", "research"],
            "investment": ["excel", "financial modeling", "sql", "communication", "risk analysis", "research"],
            "marketing manager": ["communication", "seo", "sem", "content strategy", "analytics", "google analytics"],
            "marketing": ["communication", "seo", "sem", "content strategy", "analytics", "social media"],
            "finance": ["excel", "financial modeling", "accounting", "financial reporting", "taxation", "communication"],
            "hr": ["communication", "problem solving", "presentation", "excel", "interviewing", "teamwork"],
            "human resources": ["communication", "problem solving", "excel", "payroll", "labor law", "training and development"],
            "operations": ["leadership", "project management", "problem solving", "communication", "excel", "lean management"],
            "supply chain": ["supply chain management", "procurement", "inventory management", "excel", "negotiation", "logistics management"],
            "entrepreneur": ["communication", "leadership", "problem solving", "strategic thinking", "financial planning", "presentation"],
            "product manager": ["communication", "agile", "jira", "product management", "user research", "roadmapping"],
            "sales": ["communication", "negotiation", "crm", "lead generation", "b2b sales", "presentation"],
            "account manager": ["communication", "negotiation", "crm", "client relationship management", "excel"],
        }

        for role, defaults in role_defaults.items():
            if role in normalized:
                required_skills.extend(defaults)
                break

    if not required_skills:
        required_skills = ["communication", "problem solving", "teamwork", "presentation", "leadership"]

    return _unique(required_skills)[:20]


from __future__ import annotations


# Skill learning resources and metadata
SKILL_RESOURCES: dict[str, dict] = {
    "python": {
        "difficulty": "beginner",
        "time_weeks": 8,
        "resources": [
            "Python Official Tutorials (python.org)",
            "Codecademy - Python Course (4 weeks)",
            "DataCamp - Python for Data Science (6 weeks)",
        ],
        "certifications": ["CompTIA A+", "AWS Certified Cloud Practitioner"],
    },
    "javascript": {
        "difficulty": "beginner",
        "time_weeks": 6,
        "resources": [
            "MDN Web Docs - JavaScript Guide",
            "freeCodeCamp - JavaScript Course (4 weeks)",
            "Codecademy - JavaScript Course (6 weeks)",
        ],
        "certifications": ["Google JavaScript Developer Certification"],
    },
    "react": {
        "difficulty": "intermediate",
        "time_weeks": 6,
        "resources": [
            "React Official Documentation",
            "Scrimba - React Course (4 weeks)",
            "Udemy - React Course by Stephen Grider (8 weeks)",
        ],
        "certifications": ["Meta Front-End Developer Certificate"],
    },
    "typescript": {
        "difficulty": "intermediate",
        "time_weeks": 4,
        "resources": [
            "TypeScript Official Handbook",
            "Pluralsight - TypeScript TypeScript Course (3 weeks)",
            "Codecademy - TypeScript Course (4 weeks)",
        ],
        "certifications": [],
    },
    "fastapi": {
        "difficulty": "intermediate",
        "time_weeks": 4,
        "resources": [
            "FastAPI Official Documentation",
            "Real Python - FastAPI Guide (2 weeks)",
            "Udemy - FastAPI Course (4 weeks)",
        ],
        "certifications": [],
    },
    "docker": {
        "difficulty": "intermediate",
        "time_weeks": 3,
        "resources": [
            "Docker Official Documentation",
            "Udemy - Docker Course (3 weeks)",
            "Linux Academy - Docker Course (2 weeks)",
        ],
        "certifications": ["Docker Certified Associate (DCA)"],
    },
    "kubernetes": {
        "difficulty": "advanced",
        "time_weeks": 10,
        "resources": [
            "Kubernetes Official Documentation",
            "Linux Academy - Kubernetes Course (8 weeks)",
            "Udemy - Kubernetes Course (12 weeks)",
        ],
        "certifications": ["Certified Kubernetes Administrator (CKA)"],
    },
    "aws": {
        "difficulty": "intermediate",
        "time_weeks": 8,
        "resources": [
            "AWS Official Training",
            "A Cloud Guru - AWS Solutions Architect Course (8 weeks)",
            "Udemy - AWS Certified Solutions Architect (10 weeks)",
        ],
        "certifications": ["AWS Certified Solutions Architect Associate", "AWS Certified Developer"],
    },
    "sql": {
        "difficulty": "beginner",
        "time_weeks": 4,
        "resources": [
            "SQLZoo Interactive Tutorial",
            "Udacity - SQL for Data Analysis (3 weeks)",
            "Codecademy - SQL Course (4 weeks)",
        ],
        "certifications": [],
    },
    "machine learning": {
        "difficulty": "advanced",
        "time_weeks": 12,
        "resources": [
            "Coursera - Machine Learning by Andrew Ng (8 weeks)",
            "Fast.ai - Practical Deep Learning (12 weeks)",
            "Udacity - Machine Learning Nanodegree (16 weeks)",
        ],
        "certifications": ["Google Cloud Professional Data Engineer", "AWS Certified Machine Learning Specialty"],
    },
    "communication": {
        "difficulty": "beginner",
        "time_weeks": 4,
        "resources": [
            "Toastmasters International",
            "Coursera - Communication Skills Course (3 weeks)",
            "MasterClass - Communication with Malcolm Gladwell",
        ],
        "certifications": [],
    },
    "leadership": {
        "difficulty": "intermediate",
        "time_weeks": 8,
        "resources": [
            "Coursera - Leadership and Management (6 weeks)",
            "LinkedIn Learning - Leadership Skills",
            "Udemy - Leadership Development Course (8 weeks)",
        ],
        "certifications": ["Project Management Institute (PMI)"],
    },
    "project management": {
        "difficulty": "intermediate",
        "time_weeks": 10,
        "resources": [
            "PMI - Project Management Professional (PMP)",
            "Coursera - Project Management Specialization (8 weeks)",
            "Udemy - Project Management Course (10 weeks)",
        ],
        "certifications": ["PMP", "CAPM"],
    },
    "data analysis": {
        "difficulty": "beginner",
        "time_weeks": 6,
        "resources": [
            "DataCamp - Data Analysis Course (6 weeks)",
            "Google Analytics Academy",
            "Coursera - Data Analysis Specialization (8 weeks)",
        ],
        "certifications": ["Google Analytics Certification", "Microsoft Certified: Data Analyst"],
    },
    "excel": {
        "difficulty": "beginner",
        "time_weeks": 2,
        "resources": [
            "Microsoft Excel Official Training",
            "Udemy - Excel Masterclass (2 weeks)",
            "LinkedIn Learning - Excel Essential Training",
        ],
        "certifications": ["Microsoft Office Specialist"],
    },
    "git": {
        "difficulty": "beginner",
        "time_weeks": 2,
        "resources": [
            "Official Git Documentation",
            "Codecademy - Learn Git (1 week)",
            "GitHub Learning Lab",
        ],
        "certifications": [],
    },
    "content writing": {
        "difficulty": "beginner",
        "time_weeks": 4,
        "resources": [
            "Copyblogger - Content Writing Guide",
            "Coursera - Writing in the Sciences (4 weeks)",
            "Udemy - Content Writing Course (4 weeks)",
        ],
        "certifications": ["Google Digital Garage Certificate"],
    },
    "seo": {
        "difficulty": "beginner",
        "time_weeks": 4,
        "resources": [
            "Moz - SEO Basics",
            "Semrush Academy - SEO Courses",
            "Coursera - SEO Fundamentals (4 weeks)",
        ],
        "certifications": [],
    },
    "problem solving": {
        "difficulty": "beginner",
        "time_weeks": 6,
        "resources": [
            "LeetCode - Practice Problems",
            "HackerRank - Problem Solving",
            "Udemy - Problem Solving Course (6 weeks)",
        ],
        "certifications": [],
    },
    "accounting": {
        "difficulty": "intermediate",
        "time_weeks": 12,
        "resources": [
            "AICPA - Accounting Resources",
            "Coursera - Accounting Specialization (12 weeks)",
            "Udemy - Accounting Course (12 weeks)",
        ],
        "certifications": ["CPA", "CMA"],
    },
    "legal research": {
        "difficulty": "intermediate",
        "time_weeks": 10,
        "resources": [
            "Law School Resources",
            "Coursera - Legal Research Course (8 weeks)",
            "LexisNexis Training",
        ],
        "certifications": [],
    },
}


def _get_skill_priority(skill: str, missing_skills: list[str], required_skills: list[str]) -> int:
    """Calculate priority score for a skill (1-5, where 5 is highest priority)."""
    if skill not in missing_skills:
        return 0

    # Skills appear more frequently = higher priority
    skill_importance = required_skills.count(skill) + missing_skills.count(skill)

    # Shorter learning time = higher priority
    resource = SKILL_RESOURCES.get(skill.lower(), {})
    time_weeks = resource.get("time_weeks", 8)
    time_factor = max(0, 5 - (time_weeks // 3))

    # Easier skills = slightly higher priority to start
    difficulty = resource.get("difficulty", "intermediate")
    difficulty_factor = {"beginner": 2, "intermediate": 1, "advanced": 0}.get(difficulty, 1)

    priority = min(5, max(1, skill_importance + time_factor + difficulty_factor))
    return priority


def generate_upskilling_roadmap(
    missing_skills: list[str],
    required_skills: list[str],
) -> dict:
    """
    Generate an upskilling roadmap for missing skills.
    
    Returns a dict with:
    - total_weeks: estimated time to learn all skills
    - priority_order: list of skills ordered by priority
    - skills_roadmap: details for each skill with resources and timeline
    """
    if not missing_skills:
        return {
            "total_weeks": 0,
            "priority_order": [],
            "skills_roadmap": [],
            "message": "No missing skills detected. You're ready to apply!",
        }

    # Calculate priority for each missing skill
    skill_priorities: list[tuple[str, int]] = []
    for skill in missing_skills:
        priority = _get_skill_priority(skill, missing_skills, required_skills)
        skill_priorities.append((skill, priority))

    # Sort by priority (descending)
    skill_priorities.sort(key=lambda x: (-x[1], x[0]))

    priority_order = [skill for skill, _ in skill_priorities]
    total_weeks = 0
    skills_roadmap = []

    for skill in priority_order:
        resource = SKILL_RESOURCES.get(skill.lower(), {
            "difficulty": "intermediate",
            "time_weeks": 8,
            "resources": [f"Search for '{skill}' online courses"],
            "certifications": [],
        })

        time_weeks = resource.get("time_weeks", 8)
        total_weeks += time_weeks

        skills_roadmap.append({
            "skill": skill,
            "difficulty": resource.get("difficulty"),
            "estimated_weeks": time_weeks,
            "resources": resource.get("resources", []),
            "certifications": resource.get("certifications", []),
            "priority": "high" if skill_priorities[priority_order.index(skill)][1] >= 4 else "medium" if skill_priorities[priority_order.index(skill)][1] >= 2 else "low",
        })

    return {
        "total_weeks": total_weeks,
        "priority_order": priority_order,
        "skills_roadmap": skills_roadmap,
        "message": f"Estimated time to learn all {len(missing_skills)} skills: {total_weeks} weeks ({total_weeks // 4} months)",
    }

from __future__ import annotations

import json
from pathlib import Path


ROLES_PATH = Path(__file__).resolve().parents[2] / "data" / "job_roles.json"


def _load_job_roles() -> list[dict]:
    """Load job roles database."""
    try:
        with ROLES_PATH.open("r", encoding="utf-8") as file:
            return json.load(file)
    except Exception:
        return []


def detect_role_type(job_role: str) -> str:
    """Detect the type of job role from job description or role name."""
    normalized = job_role.lower()

    # Categorize by role family
    healthcare_keywords = ["healthcare", "nurse", "doctor", "hospital", "medical", "clinical", "patient"]
    legal_keywords = ["legal", "lawyer", "law", "attorney", "paralegal", "counsel"]
    education_keywords = ["teacher", "education", "instructor", "professor", "faculty"]
    business_keywords = ["sales", "business", "manager", "product", "account", "marketing"]
    design_keywords = ["design", "ux", "ui", "creative", "graphic", "visual"]
    technical_keywords = ["engineer", "developer", "programmer", "software", "backend", "frontend", "full stack"]

    # Check for medical/healthcare roles
    if any(word in normalized for word in healthcare_keywords):
        return "healthcare"
    # Check for legal roles
    elif any(word in normalized for word in legal_keywords):
        return "legal"
    # Check for education roles
    elif any(word in normalized for word in education_keywords):
        return "education"
    # Check for design roles
    elif any(word in normalized for word in design_keywords):
        return "design"
    # Check for business roles
    elif any(word in normalized for word in business_keywords):
        return "business"
    # Check for technical roles
    elif any(word in normalized for word in technical_keywords):
        return "technical"
    else:
        return "general"


def _get_role_specific_feedback(
    role_type: str,
    matched_skills: list[str],
    missing_skills: list[str],
    weak_sections: list[str],
    job_role: str,
) -> dict:
    """Generate role-specific feedback based on detected job type."""

    feedback_templates = {
        "healthcare": {
            "improvements": [
                f"Highlight patient care experience and clinical expertise relevant to {job_role or 'healthcare roles'}.",
                "Include certifications, licenses, and compliance training prominently.",
                "Emphasize teamwork, communication with patients/colleagues, and crisis management.",
            ],
            "priority_actions": [
                "Add specific patient outcomes, procedures, and clinical competencies to experience bullets.",
                "Include relevant healthcare certifications and continuing education credits.",
                "Highlight safety protocols, HIPAA compliance, and quality improvement initiatives.",
            ],
            "interview_questions": [
                f"Describe a challenging patient case and how you handled it in your {job_role or 'healthcare'} role.",
                "How do you prioritize patient safety and maintain confidentiality?",
                "Tell us about a time you had to work as part of a multidisciplinary healthcare team.",
            ],
        },
        "legal": {
            "improvements": [
                f"Emphasize legal expertise, case types, and precedents relevant to {job_role or 'legal roles'}.",
                "Include bar admissions, law school, and specialized certifications.",
                "Highlight written communication, research skills, and negotiation experience.",
            ],
            "priority_actions": [
                "Detail specific legal matters, case outcomes, and legal areas of expertise.",
                "Include bar status, jurisdictions, and any notable case wins or publications.",
                "Emphasize attention to detail, legal research skills, and compliance knowledge.",
            ],
            "interview_questions": [
                f"Describe a complex legal matter you handled and the outcome in your {job_role or 'legal'} work.",
                "How do you stay current with changes in law and regulations?",
                "Tell us about your experience with legal research and writing.",
            ],
        },
        "education": {
            "improvements": [
                f"Highlight teaching methods, student outcomes, and curriculum development for {job_role or 'education'}.",
                "Include relevant degrees, certifications, and professional development.",
                "Emphasize classroom management, communication, and student engagement strategies.",
            ],
            "priority_actions": [
                "Add specific achievements like student performance improvements, test score gains.",
                "Include professional certifications, subject matter expertise, and teaching innovations.",
                "Highlight your approach to inclusive education and supporting diverse learners.",
            ],
            "interview_questions": [
                f"How do you engage students and create an effective learning environment in {job_role or 'your field'}?",
                "Describe your teaching philosophy and how you measure student success.",
                "What strategies do you use to support students with different learning styles?",
            ],
        },
        "business": {
            "improvements": [
                f"Emphasize business acumen, sales/revenue impact, and market knowledge for {job_role or 'business roles'}.",
                "Include metrics: revenue generated, growth percentages, accounts managed.",
                "Highlight strategic planning, negotiation, and relationship management skills.",
            ],
            "priority_actions": [
                "Add quantifiable business outcomes: 'increased revenue by X%', 'grew client base by Y'.",
                "Include industry knowledge, competitive analysis, and market trends awareness.",
                "Emphasize leadership, team building, and client retention achievements.",
            ],
            "interview_questions": [
                f"How have you contributed to business growth and profitability in your {job_role or 'business'} role?",
                "Describe your approach to building and maintaining client relationships.",
                "Tell us about a successful negotiation or deal you've led.",
            ],
        },
        "design": {
            "improvements": [
                f"Showcase portfolio work, design tools, and aesthetic sensibility for {job_role or 'design roles'}.",
                "Include design software proficiencies, design methodologies, and awards.",
                "Highlight user research, prototyping, and iterative design process experience.",
            ],
            "priority_actions": [
                "Add specific design projects with visual impact and user engagement metrics.",
                "Include proficiency in tools (Figma, Adobe Creative Suite, Sketch, Prototyping tools).",
                "Emphasize UX research, user testing, and iterative design improvements.",
            ],
            "interview_questions": [
                f"Walk us through your design process for a major project in your {job_role or 'design'} work.",
                "How do you balance aesthetics with functionality and user experience?",
                "How do you incorporate user feedback and user testing into your design decisions?",
            ],
        },
        "technical": {
            "improvements": [
                f"Highlight technical projects, programming languages, and technologies for {job_role or 'technical roles'}.",
                "Include open-source contributions, technical blogs, and GitHub portfolio.",
                "Emphasize problem-solving approach, scalability considerations, and optimization.",
            ],
            "priority_actions": [
                "Add specific technical achievements: 'reduced API response time by 40%', 'deployed X feature'.",
                "Include relevant certifications and continuous learning (courses, certifications).",
                "Highlight code quality, testing practices, and collaboration with other engineers.",
            ],
            "interview_questions": [
                f"Describe a complex technical problem you solved in your {job_role or 'technical'} work.",
                "How do you approach learning new technologies and frameworks?",
                "Tell us about your experience with code reviews, testing, and deployment practices.",
            ],
        },
        "general": {
            "improvements": [
                f"Tailor the summary and experience to the {job_role or 'target'} role.",
                "Add measurable impact and results to each role and achievement.",
                "Place most relevant experience and accomplishments near the top.",
            ],
            "priority_actions": [
                "Emphasize achievements with quantifiable results and business impact.",
                "Customize experience bullets and skills for the target role and industry.",
                "Improve ATS compatibility with clear formatting and relevant keywords.",
            ],
            "interview_questions": [
                f"How does your background prepare you for the {job_role or 'target'} role?",
                "What achievement are you most proud of in your career?",
                "Why are you interested in this specific role and company?",
            ],
        },
    }

    # Get role-specific template or use general
    template = feedback_templates.get(role_type, feedback_templates["general"])

    return {
        "improvements": template["improvements"],
        "priority_actions": template["priority_actions"],
        "interview_questions": template["interview_questions"],
    }


def get_role_specific_fallback_feedback(
    job_role: str,
    matched_skills: list[str],
    missing_skills: list[str],
    weak_sections: list[str],
) -> dict:
    """Get role-specific fallback feedback."""
    role_type = detect_role_type(job_role)

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

    role_specific = _get_role_specific_feedback(role_type, matched_skills, missing_skills, weak_sections, job_role)

    rewritten_bullets = {
        "healthcare": [
            "Provided direct patient care, monitoring vitals and implementing care plans with documented patient satisfaction.",
            "Collaborated with clinical team to develop and execute patient care protocols improving patient outcomes.",
        ],
        "legal": [
            "Successfully defended client interests in complex litigation, achieving favorable settlement and legal outcomes.",
            "Conducted thorough legal research and drafted comprehensive legal briefs with sound legal precedent.",
        ],
        "education": [
            "Developed innovative curriculum improving student test scores by 18% and overall class engagement.",
            "Mentored struggling students using personalized learning plans, improving student success metrics.",
        ],
        "business": [
            "Increased territory revenue by 25% through strategic relationship management and client account expansion.",
            "Led cross-functional business initiative to launch new product line, achieving business targets.",
        ],
        "design": [
            "Redesigned user interface improving user engagement metrics and reducing user bounce rates.",
            "Conducted user research and testing, iterating design based on feedback for optimal user experience.",
        ],
        "technical": [
            "Architected system platform handling high-volume requests with strong uptime and system reliability.",
            "Optimized technical processes and systems reducing latency, improving user experience and efficiency.",
        ],
        "general": [
            "Led project from conception to completion, delivering results on schedule within budget constraints.",
            "Collaborated with teams to achieve organizational goals and improve operational efficiency.",
        ],
    }.get(role_type, [
        "Led project from conception to completion, delivering results on schedule within budget constraints.",
        "Collaborated with teams to achieve organizational goals and improve operational efficiency.",
    ])

    return {
        "source": "fallback",
        "role_type": role_type,
        "strengths": strengths,
        "weaknesses": weaknesses or ["No major weaknesses detected in the current MVP analysis."],
        "improvements": role_specific.get("improvements", []),
        "priority_actions": role_specific.get("priority_actions", []),
        "rewritten_bullets": rewritten_bullets,
        "interview_questions": role_specific.get("interview_questions", []),
    }

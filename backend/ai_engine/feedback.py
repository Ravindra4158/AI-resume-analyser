from __future__ import annotations


def generate_feedback(
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
        strengths.append("The resume has a starting structure that can be shaped toward the target role.")

    weaknesses = []
    if missing_skills:
        weaknesses.append(
            "Add evidence for missing role skills: " + ", ".join(missing_skills[:8]) + "."
        )
    if weak_sections:
        weaknesses.append(
            "Strengthen these sections: " + ", ".join(weak_sections) + "."
        )

    improvements = [
        f"Tailor the summary and top skills to the {job_role or 'target'} role.",
        "Convert responsibilities into impact bullets with metrics, tools, and outcomes.",
        "Place the most relevant projects and experience near the top of the resume.",
    ]

    rewritten_bullets = [
        "Built and improved a project using relevant tools, reducing manual effort and improving user workflow.",
        "Collaborated with teammates to deliver features, debug issues, and document technical decisions.",
    ]

    return {
        "strengths": strengths,
        "weaknesses": weaknesses or ["No major weaknesses detected in the current MVP analysis."],
        "improvements": improvements,
        "rewritten_bullets": rewritten_bullets,
    }


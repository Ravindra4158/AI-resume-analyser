from __future__ import annotations


SECTION_KEYWORDS = {
    "experience": ["experience", "work history", "employment", "internship"],
    "projects": ["projects", "portfolio", "github"],
    "education": ["education", "degree", "university", "college"],
}


def find_weak_sections(resume_text: str) -> list[str]:
    normalized = resume_text.lower()
    weak_sections: list[str] = []

    for section, keywords in SECTION_KEYWORDS.items():
        if not any(keyword in normalized for keyword in keywords):
            weak_sections.append(section)

    if len(resume_text.split()) < 250:
        weak_sections.append("resume detail")

    return weak_sections


from __future__ import annotations

import re


def analyze_ats_compliance(resume_text: str) -> dict:
    """
    Analyze resume ATS (Applicant Tracking System) compliance.
    
    Returns a dict with:
    - score: 0-100 ATS compliance score
    - issues: list of detected ATS problems
    - recommendations: list of improvement suggestions
    """
    issues: list[str] = []
    recommendations: list[str] = []
    score = 100

    normalized = resume_text.lower()
    lines = resume_text.split("\n")
    word_count = len(resume_text.split())

    # Check 1: Resume has minimum content
    if word_count < 100:
        issues.append("Resume is too short (less than 100 words)")
        recommendations.append("Expand resume with more experience, skills, and achievements (aim for 200-500 words)")
        score -= 15

    # Check 2: Look for section headers (indicates good structure)
    section_headers = ["experience", "education", "skills", "projects", "summary", "objective"]
    found_headers = sum(1 for header in section_headers if header in normalized)
    if found_headers < 3:
        issues.append("Missing clear section headers (resume structure unclear)")
        recommendations.append("Add clear section headers like 'Experience', 'Education', 'Skills', 'Projects'")
        score -= 10

    # Check 3: Check for unusual characters or formatting
    special_chars = len(re.findall(r"[®™©℠€¥£¢]", resume_text))
    if special_chars > 2:
        issues.append("Contains excessive special characters that may not parse correctly")
        recommendations.append("Replace special characters with plain text. Use '*' or '-' for bullets instead")
        score -= 8

    # Check 4: Check for typical contact info (helps ATS identify candidate)
    has_email = bool(re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", resume_text))
    has_phone = bool(re.search(r"(\+\d{1,3}[-.\s]?)?\(\d{3}\)[-.\s]?\d{3}[-.\s]?\d{4}|\d{10}", resume_text))

    if not has_email:
        issues.append("Email address not detected")
        recommendations.append("Add email address in clear format: name@example.com")
        score -= 8

    if not has_phone:
        issues.append("Phone number not detected")
        recommendations.append("Add phone number in clear format: +1 (XXX) XXX-XXXX")
        score -= 5

    # Check 5: Look for dates (ATS uses dates for timeline)
    date_pattern = r"\b(20\d{2}|19\d{2}|\d{1,2}/\d{1,2}/\d{4}|\d{4}-\d{2}-\d{2})\b"
    dates_found = len(re.findall(date_pattern, resume_text))
    if dates_found < 2:
        issues.append("Few or no dates found (timeline unclear)")
        recommendations.append("Add dates to experience and education entries (e.g., 'Jan 2020 - Dec 2021')")
        score -= 10

    # Check 6: Look for line breaks/excessive formatting
    blank_lines = len([line for line in lines if line.strip() == ""])
    if blank_lines > len(lines) / 3:
        issues.append("Excessive blank lines or formatting may confuse ATS")
        recommendations.append("Reduce blank lines. Use single-line breaks between sections")
        score -= 5

    # Check 7: Check for proper bullet point format
    bullet_chars = len(re.findall(r"^[\s]*[-•*]\s", resume_text, re.MULTILINE))
    if bullet_chars == 0 and word_count > 200:
        issues.append("No bullet points detected (hard to scan)")
        recommendations.append("Use bullet points to format achievements and responsibilities")
        score -= 8

    # Check 8: Look for file-specific artifacts (tables, columns)
    if "table" in normalized or "column" in normalized:
        issues.append("Resume may contain tables/columns that don't parse in ATS")
        recommendations.append("Remove tables. Use simple text format with bullet points")
        score -= 10

    # Check 9: Check for uncommon fonts or encoding
    if any(char.isalpha() and ord(char) > 127 for char in resume_text):
        issues.append("Non-ASCII characters detected (may not parse correctly)")
        recommendations.append("Use only standard ASCII characters. Replace accented letters if possible")
        score -= 5

    # Check 10: Keywords density (more keywords = better ATS score)
    common_keywords = ["experience", "education", "skills", "project", "achievement", "responsibility", "managed", "developed"]
    keyword_score = sum(1 for kw in common_keywords if kw in normalized)
    if keyword_score < 3:
        issues.append("Low keyword density (resume may be filtered out)")
        recommendations.append("Use action verbs: 'developed', 'managed', 'led', 'improved', 'implemented'")
        score -= 5

    score = max(0, min(100, score))

    return {
        "score": score,
        "issues": issues,
        "recommendations": recommendations,
    }

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


def _ats_score(resume_text: str) -> int:  # noqa: C901
    """
    Strict ATS score — simulates a seasoned recruiter with 30 years of
    experience who has zero patience for fluff, bad formatting, or vague
    language.

    Scoring philosophy
    ------------------
    - You START at 0 and EARN points. Nothing is given for free.
    - Most average resumes score 35-60.
    - Only genuinely well-crafted, ATS-optimised resumes score 80+.
    - Deductions are real and punishing.

    Max raw points = 110, capped to 0-100 after all deductions.
    """
    text = resume_text
    lower = text.lower()
    word_count = len(text.split())
    score = 0
    deductions = 0

    # ── CONTACT COMPLETENESS (max 25 pts) ──────────────────────────
    # Recruiter can't call you if you forgot your number.

    if re.search(r"[\w.\-+]+@[\w.-]+\.\w{2,}", text):
        score += 10
    else:
        deductions += 10  # uncontactable — hard pass

    if re.search(r"(\+?\d[\d\s().\-]{7,}\d)", text):
        score += 10
    else:
        deductions += 5

    # LinkedIn expected in today's market
    if re.search(r"linkedin\.com/in/", lower):
        score += 5
    else:
        deductions += 3

    # ── STRUCTURE & SECTIONS (max 25 pts) ──────────────────────────
    # ATS parses by section headers. Missing headers = invisible content.

    # Skills section — mandatory
    if re.search(r"\b(technical skills?|key skills?|core competencies|skills?)\b", lower):
        score += 8
    else:
        deductions += 10  # no skills section = ATS rejects instantly

    # Experience section — mandatory
    if re.search(r"\b(work experience|professional experience|experience|employment history|internship)\b", lower):
        score += 8
    else:
        deductions += 10

    # Education section
    if re.search(r"\b(education|academic|degree|university|college|b\.tech|mba|bca|bba|bachelor|master)\b", lower):
        score += 5
    else:
        deductions += 5

    # Summary / Objective — sets the tone
    if re.search(r"\b(career summary|professional summary|summary|objective|profile|about me|career objective)\b", lower):
        score += 4
    else:
        deductions += 4  # recruiter has zero context about you at first glance

    # ── CONTENT QUALITY (max 30 pts) ───────────────────────────────
    # This is where 90% of candidates fail. Vague = worthless.

    # Quantifiable achievements — the ONLY thing that actually matters
    metrics = re.findall(
        r"(\d+\s*%|\$\s*[\d,]+|\d+\s*x\b|\d+\s*(users?|clients?|customers?|employees?|"
        r"projects?|years?|months?|weeks?|days?|crores?|lakhs?|million|billion|k\b|hours?))",
        lower,
    )
    metric_count = len(metrics)
    if metric_count >= 5:
        score += 15       # impressive impact statements
    elif metric_count >= 3:
        score += 10
    elif metric_count >= 1:
        score += 5
    else:
        deductions += 8   # zero numbers = "I was responsible for things" writing

    # Strong action verbs — ownership vs passivity
    strong_verbs = [
        "achieved", "accelerated", "automated", "analysed", "analyzed",
        "built", "boosted", "collaborated", "conceptualised", "conceptualized",
        "coordinated", "created", "cut", "delivered", "deployed", "designed",
        "developed", "directed", "drove", "eliminated", "engineered", "established",
        "exceeded", "executed", "generated", "grew", "implemented", "improved",
        "increased", "initiated", "launched", "led", "managed", "mentored",
        "migrated", "negotiated", "optimised", "optimized", "orchestrated",
        "overhauled", "pioneered", "produced", "reduced", "refactored",
        "researched", "restructured", "revamped", "saved", "scaled",
        "secured", "shaped", "shipped", "simplified", "spearheaded",
        "streamlined", "transformed", "trained", "won",
    ]
    verb_hits = sum(1 for v in strong_verbs if v in lower)
    if verb_hits >= 8:
        score += 10
    elif verb_hits >= 4:
        score += 6
    elif verb_hits >= 2:
        score += 3
    else:
        deductions += 6   # "worked on" and "helped with" — recruiter is asleep

    # Projects / portfolio
    if re.search(r"\b(projects?|portfolio|github\.com|gitlab\.com|live demo|deployed)\b", lower):
        score += 5
    else:
        deductions += 3

    # ── RESUME LENGTH & SUBSTANCE (max 15 pts) ─────────────────────
    # Too short = nothing to say. Too long = can't edit yourself.
    if 350 <= word_count <= 800:
        score += 15       # the sweet spot
    elif 250 <= word_count < 350:
        score += 8        # a bit thin
    elif 800 < word_count <= 1200:
        score += 8        # a bit verbose
    elif 150 <= word_count < 250:
        score += 4
        deductions += 5   # suspiciously thin
    else:
        deductions += 12  # either a haiku or a novel — both are wrong

    # ── ATS FORMATTING PENALTIES (deductions only) ─────────────────
    # Real ATS systems choke on these; recruiter never sees your resume.

    # Non-ASCII / emojis / icons
    non_ascii_count = len(re.findall(r"[^\x00-\x7F]", text))
    if non_ascii_count > 50:
        deductions += 10  # icon-heavy resume — ATS nightmare
    elif non_ascii_count > 20:
        deductions += 5

    # Tables and column formatting
    if text.count("|") > 12:
        deductions += 8   # tables = garbled text in most ATS parsers
    elif text.count("|") > 5:
        deductions += 4
    if text.count("\t") > 20:
        deductions += 5

    # Fragmented short lines (multi-column PDF extraction artifact)
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    if lines:
        short_line_ratio = sum(1 for ln in lines if len(ln) < 12) / len(lines)
        if short_line_ratio > 0.55:
            deductions += 8   # column-parsed garbage
        elif short_line_ratio > 0.35:
            deductions += 4

    # Personal pronouns (resumes should be implied 3rd person)
    pronoun_count = len(re.findall(r"\b(i am|i have|i worked|i built|i led|my responsibilities)\b", lower))
    if pronoun_count >= 3:
        deductions += 5
    elif pronoun_count >= 1:
        deductions += 2

    # Clichés that add zero value
    cliches = [
        "team player", "detail-oriented", "hard worker", "passionate about",
        "go-getter", "results-driven", "dynamic professional", "synergy",
        "think outside the box", "proactive", "self-starter", "fast learner",
        "good communication skills", "eager to learn",
    ]
    cliche_hits = sum(1 for c in cliches if c in lower)
    if cliche_hits >= 4:
        deductions += 8   # buzzword bingo card
    elif cliche_hits >= 2:
        deductions += 4
    elif cliche_hits >= 1:
        deductions += 2

    # ── FINAL TALLY ────────────────────────────────────────────────
    final = score - deductions
    return max(0, min(100, final))

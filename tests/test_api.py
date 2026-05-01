

from __future__ import annotations

from fastapi.testclient import TestClient

from main import app
from analyzer.skills import infer_required_skills
from ai_engine.upskilling import generate_upskilling_roadmap
from ai_engine.role_feedback import detect_role_type, get_role_specific_fallback_feedback
client = TestClient(app)


def test_health_returns_status_metadata() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert "version" in response.json()
    assert "environment" in response.json()


def test_analyze_txt_resume_returns_score() -> None:
    resume = """
    Priya Sharma
    priya@example.com | +91 98765 43210

    Skills
    React, JavaScript, TypeScript, HTML, CSS, Tailwind, API, Git, GitHub

    Experience
    Built React dashboards connected to API services.

    Projects
    Resume Analyzer Dashboard

    Education
    B.Tech Computer Science
    """

    response = client.post(
        "/analyze",
        files={"resume": ("resume.txt", resume, "text/plain")},
        data={"job_role": "Frontend Developer React JavaScript TypeScript HTML CSS Tailwind API Git GitHub"},
    )

    payload = response.json()
    assert response.status_code == 200
    assert payload["score"]["overall"] >= 80
    assert "react" in payload["matched_skills"]
    assert payload["feedback"]["improvements"]
    assert payload["feedback"]["priority_actions"]
    assert payload["feedback"]["rewritten_bullets"]
    assert payload["feedback"]["interview_questions"]
    assert payload["feedback"]["source"] == "fallback"


def test_analyze_rejects_unsupported_file_type() -> None:
    response = client.post(
        "/analyze",
        files={"resume": ("resume.exe", b"not a resume", "application/octet-stream")},
        data={"job_role": "Frontend Developer"},
    )

    assert response.status_code == 400
    assert response.json()["error"]["message"] == "Please upload a PDF, DOCX, or TXT resume."


def test_analyze_rejects_empty_resume() -> None:
    response = client.post(
        "/analyze",
        files={"resume": ("resume.txt", b"", "text/plain")},
        data={"job_role": "Frontend Developer"},
    )

    assert response.status_code == 400
    assert response.json()["error"]["message"] == "Resume text is empty."


def test_infer_required_skills_chooses_role_bundle_for_hybrid_jd() -> None:
    jd = """
    Senior Full Stack Engineer
    Build React and TypeScript user interfaces, REST APIs in Python and FastAPI,
    and deploy services with Docker and AWS.
    """

    required_skills = infer_required_skills(jd)

    assert "react" in required_skills
    assert "python" in required_skills
    assert "docker" in required_skills
    assert "aws" in required_skills


def test_infer_required_skills_falls_back_to_broader_non_technical_role() -> None:
    jd = "Product Manager responsible for roadmap planning, stakeholder communication, and agile delivery."

    required_skills = infer_required_skills(jd)

    assert "communication" in required_skills
    assert "agile" in required_skills


def test_infer_required_skills_supports_non_engineering_roles() -> None:
    jd = "Marketing Specialist needed for social media campaigns, content writing, SEO, and presentation work."

    required_skills = infer_required_skills(jd)

    assert "social media" in required_skills
    assert "content writing" in required_skills
    assert "seo" in required_skills


def test_infer_required_skills_supports_healthcare_roles() -> None:
    jd = "Registered Nurse needed for patient care, medical records, teamwork, and safety compliance in a clinical setting."

    required_skills = infer_required_skills(jd)

    assert "patient care" in required_skills
    assert "medical records" in required_skills
    assert "safety compliance" in required_skills


def test_infer_required_skills_supports_legal_roles() -> None:
    jd = "Paralegal required for legal research, drafting, documentation, and case preparation."

    required_skills = infer_required_skills(jd)

    assert "legal research" in required_skills
    assert "drafting" in required_skills
    assert "documentation" in required_skills


def test_analyze_includes_ats_compliance_data() -> None:
    resume = """
    John Smith
    john@example.com | (555) 123-4567

    Experience
    Developed software solutions from 2020 to 2022.
    Managed team projects and delivered results.

    Skills
    Python, JavaScript, Project Management, Communication

    Education
    B.S. Computer Science, 2020
    """

    response = client.post(
        "/analyze",
        files={"resume": ("resume.txt", resume, "text/plain")},
        data={"job_role": "Software Developer"},
    )

    payload = response.json()
    assert response.status_code == 200
    assert "ats_compliance" in payload
    assert "score" in payload["ats_compliance"]
    assert "issues" in payload["ats_compliance"]
    assert "recommendations" in payload["ats_compliance"]
    assert 0 <= payload["ats_compliance"]["score"] <= 100


def test_analyze_includes_upskilling_roadmap() -> None:
    resume = """
    Jane Doe
    jane@example.com | (555) 987-6543

    Skills
    Python, Excel

    Experience
    Python developer for 2 years
    """

    response = client.post(
        "/analyze",
        files={"resume": ("resume.txt", resume, "text/plain")},
        data={"job_role": "Full Stack Developer with React, Docker, AWS needed"},
    )

    payload = response.json()
    assert response.status_code == 200
    assert "upskilling_roadmap" in payload
    assert "total_weeks" in payload["upskilling_roadmap"]
    assert "priority_order" in payload["upskilling_roadmap"]
    assert "skills_roadmap" in payload["upskilling_roadmap"]
    assert "message" in payload["upskilling_roadmap"]


def test_upskilling_roadmap_priority_ordering() -> None:
    missing = ["python", "docker", "communication"]
    required = ["python", "docker", "communication", "teamwork"] * 2

    roadmap = generate_upskilling_roadmap(missing, required)

    assert roadmap["total_weeks"] > 0
    assert len(roadmap["priority_order"]) == len(missing)
    assert len(roadmap["skills_roadmap"]) == len(missing)


def test_role_type_detection_identifies_healthcare() -> None:
    role_type = detect_role_type("Registered Nurse with patient care and medical records")
    assert role_type == "healthcare"


def test_role_type_detection_identifies_legal() -> None:
    role_type = detect_role_type("Paralegal for legal research and contract drafting")
    assert role_type == "legal"


def test_role_type_detection_identifies_technical() -> None:
    role_type = detect_role_type("Senior Software Engineer with Python and Docker")
    assert role_type == "technical"


def test_healthcare_feedback_includes_clinical_context() -> None:
    feedback = get_role_specific_fallback_feedback(
        job_role="Registered Nurse",
        matched_skills=["patient care", "communication"],
        missing_skills=["medical records", "safety compliance"],
        weak_sections=["certifications"],
    )

    assert feedback["role_type"] == "healthcare"
    assert any("patient" in item.lower() or "clinical" in item.lower() for item in feedback["improvements"])
    assert any("certification" in item.lower() or "license" in item.lower() for item in feedback["priority_actions"])
    assert feedback["rewritten_bullets"]


def test_legal_feedback_includes_legal_context() -> None:
    feedback = get_role_specific_fallback_feedback(
        job_role="Paralegal",
        matched_skills=["legal research", "writing"],
        missing_skills=["case management", "documentation"],
        weak_sections=["experience"],
    )

    assert feedback["role_type"] == "legal"
    assert any("legal" in item.lower() for item in feedback["improvements"])
    assert any("matter" in item.lower() or "bar" in item.lower() for item in feedback["priority_actions"])


def test_technical_feedback_includes_technical_context() -> None:
    feedback = get_role_specific_fallback_feedback(
        job_role="Senior Software Engineer with Python and Docker",
        matched_skills=["python", "git"],
        missing_skills=["docker", "kubernetes"],
        weak_sections=[],
    )

    assert feedback["role_type"] == "technical"
    assert any("technical" in item.lower() or "project" in item.lower() for item in feedback["improvements"])
    assert any("achievement" in item.lower() or "metric" in item.lower() for item in feedback["priority_actions"])

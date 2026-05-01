from __future__ import annotations

from fastapi.testclient import TestClient

from main import app


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

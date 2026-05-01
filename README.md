# AI Resume Analyzer

A hackathon-friendly MVP for analyzing resumes against a target role or job description.

## What Is Built

- FastAPI backend with a `/health` route and `/analyze` resume upload route.
- Resume parsing for PDF, DOCX, and TXT files.
- Keyword-based skill extraction from `data/skills_db.json`.
- Skill matching, missing skill detection, weak section detection, and weighted scoring.
- React dashboard for uploading a resume and viewing the analysis.
- Deterministic feedback engine that works without an API key.

## Project Structure

```text
backend/
  ai_engine/
  analyzer/
  parser/
  main.py
frontend/
  src/
data/
  skills_db.json
TASKS.md
plan.md
skills.md
```

## Run Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Backend runs at `http://localhost:8000`.

## Run Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at `http://localhost:5173`.

## API

`POST /analyze`

Form data:

- `resume`: PDF, DOCX, or TXT file.
- `job_role`: job role, job description, or skill list.

Returns:

- Overall score and scoring breakdown.
- Resume skills, required skills, matched skills, and missing skills.
- Weak sections and improvement feedback.

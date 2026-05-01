# AI Resume Analyzer

An AI-powered job-readiness copilot that analyzes a resume against a target role, surfaces missing skills and weak sections, and gives a practical roadmap to improve interview chances.

## What Is Built

- FastAPI backend with a `/health` route and `/analyze` resume upload route.
- Resume parsing for PDF, DOCX, and TXT files.
- Keyword-based skill extraction from `data/skills_db.json`.
- Skill matching, missing skill detection, weak section detection, and weighted scoring.
- React dashboard for uploading a resume and viewing the analysis.
- Deterministic feedback engine that works without an API key.
- Optional OpenAI-powered feedback for richer rewrite suggestions, action plans, and interview questions.

## Hackathon Pitch

Most job seekers do not know why they are being rejected. This project turns a resume into a role-specific readiness report with actionable next steps instead of giving only a generic score.

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
samples/
  strong_frontend_resume.txt
  weak_frontend_resume.txt
scripts/
  smoke_api.sh
TASKS.md
plan.md
skills.md
```

## Run Backend

Windows PowerShell:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m uvicorn main:app --reload
```

Or from the repo root:

```powershell
.\scripts\start-backend.ps1
```

macOS / Linux:

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

If the frontend shows `ECONNREFUSED 127.0.0.1:8000`, the backend is not running yet. Start it first, then retry the upload.

## Production Configuration

Backend environment variables:

- `APP_NAME`: API display name.
- `APP_VERSION`: deployed app version.
- `ENVIRONMENT`: use `production` for deployed environments.
- `ALLOWED_ORIGINS`: comma-separated frontend origins allowed by CORS.
- `MAX_UPLOAD_BYTES`: maximum resume upload size, defaults to 5 MB.
- `RESUME_PREVIEW_CHARS`: length of the returned resume preview.
- `OPENAI_API_KEY`: enables AI-generated feedback when set.
- `OPENAI_MODEL`: OpenAI model name, defaults to `gpt-5-mini`.
- `OPENAI_TIMEOUT_SECONDS`: timeout for OpenAI API calls.

Frontend environment variables:

- `VITE_API_URL`: public URL of the backend API.

## Enable AI Features

By default, the app uses deterministic fallback feedback so it always works locally.

To enable the AI features from `plan.md`, add your OpenAI API key in the backend environment:

```powershell
$env:OPENAI_API_KEY="your_api_key_here"
$env:OPENAI_MODEL="gpt-5-mini"
```

Then restart the backend and analyze a resume again.

When AI is enabled, the app can return:

- role-specific strengths and weaknesses
- priority action plan
- rewritten resume bullets
- interview prep questions

When no API key is set, the app falls back to the built-in local feedback engine.

## Test

Backend:

```bash
cd backend
source .venv/bin/activate
pip install -r requirements-dev.txt
cd ..
pytest
```

Frontend:

```bash
cd frontend
npm run build
```

## Demo Links

- Frontend: `http://localhost:5173`
- Backend health: `http://localhost:8000/health`
- Swagger API docs: `http://localhost:8000/docs`

## Try Sample Resumes

Use the files in `samples/` from the frontend upload form:

- `samples/strong_frontend_resume.txt` should produce a stronger match for a frontend role.
- `samples/weak_frontend_resume.txt` should show more missing skills and improvement feedback.

You can also test the API directly while the backend is running:

```bash
./scripts/smoke_api.sh
./scripts/smoke_api.sh samples/weak_frontend_resume.txt
```

## API

`POST /analyze`

Form data:

- `resume`: PDF, DOCX, or TXT file.
- `job_role`: job role, job description, or skill list.

Returns:

- Overall score and scoring breakdown.
- Resume skills, required skills, matched skills, and missing skills.
- Weak sections and improvement feedback.

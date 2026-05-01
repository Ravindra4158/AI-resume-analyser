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

## Production Configuration

Backend environment variables:

- `APP_NAME`: API display name.
- `APP_VERSION`: deployed app version.
- `ENVIRONMENT`: use `production` for deployed environments.
- `ALLOWED_ORIGINS`: comma-separated frontend origins allowed by CORS.
- `MAX_UPLOAD_BYTES`: maximum resume upload size, defaults to 5 MB.
- `RESUME_PREVIEW_CHARS`: length of the returned resume preview.

Frontend environment variables:

- `VITE_API_URL`: public URL of the backend API.

## Docker Deployment

Build and run both services:

```bash
docker compose up --build
```

Docker frontend runs at `http://localhost:8080`.
Docker backend runs at `http://localhost:8000`.

For a real domain, update `ALLOWED_ORIGINS` in `docker-compose.yml` and build the frontend with the deployed backend URL:

```bash
docker compose build --build-arg VITE_API_URL=https://your-api-domain.com frontend
docker compose up
```

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

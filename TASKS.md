# AI Resume Analyzer Tasks

## MVP Build

1. Backend setup
   - Create FastAPI app.
   - Add `/health` endpoint.
   - Add `/analyze` upload endpoint.

2. Resume parsing
   - Accept PDF, DOCX, TXT, and plain text uploads.
   - Extract readable resume text.
   - Normalize whitespace for analysis.

3. Skill extraction
   - Store a small skill dictionary in `data/skills_db.json`.
   - Match skills from resume text.
   - Match required skills from job role or job description.

4. Matching and scoring
   - Calculate matched and missing skills.
   - Produce a 0-100 match score.
   - Add section-based scoring for experience, projects, and ATS format.

5. Feedback engine
   - Generate strengths, weaknesses, improvements, and rewritten bullet examples.
   - Keep the first version deterministic so the app works without API keys.

6. Frontend setup
   - Create React upload form.
   - Add job role / description input.
   - Show score, matched skills, missing skills, and suggestions.

7. Demo polish
   - Add setup instructions.
   - Add sample test cases later if time allows.


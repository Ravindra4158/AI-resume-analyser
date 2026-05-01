# 🚀 AI Resume Analyzer — plan.md (Codex / Cursor Ready)

---

# 📌 Project Overview

Build an AI-powered Resume Analyzer that:

* Extracts resume content (PDF/DOCX)
* Matches it with a job role or description
* Identifies skill gaps
* Generates actionable improvement suggestions

---

# 🎯 Core Objectives

* Resume parsing (structured data)
* Job-role matching
* Skill gap detection
* AI-generated feedback + rewrite
* Clean dashboard for demo

---

# 🧠 System Architecture

```text
User → Upload Resume → Parser → Analyzer → AI Engine → Response → Frontend
```

---

# 📦 Modules Breakdown

## 1. 📄 Resume Parser (`parser/`)

**Goal:** Extract structured data from resume

### Tasks:

* Extract text from PDF/DOCX
* Clean + normalize text
* Identify:

  * Skills
  * Education
  * Experience
  * Projects

### Tools:

* `pdfplumber` / `PyMuPDF`
* `python-docx`
* Regex + NLP

---

## 2. 🔍 Skill Extractor (`analyzer/skills.py`)

**Goal:** Identify candidate skills

### Logic:

* Predefined skill dictionary
* NLP matching (keywords + phrases)

```python
SKILLS_DB = ["python", "react", "node.js", "sql", "machine learning"]
```

---

## 3. 🎯 Job Matcher (`analyzer/matcher.py`)

**Goal:** Compare resume with job role

### Input:

* Resume skills
* Job description / role

### Output:

* Match score (0–100)
* Missing skills

```python
score = matched_skills / total_required_skills * 100
```

---

## 4. 📉 Gap Analyzer (`analyzer/gap.py`)

**Goal:** Identify what’s missing

### Output:

* Missing skills list
* Weak sections (projects, experience)

---

## 5. 🧠 AI Engine (`ai_engine/`)

**Goal:** Generate smart feedback

### Prompt Template:

```
You are a senior recruiter.

Analyze this resume for the role: {job_role}

Return:
- Strengths
- Weaknesses
- Missing skills
- Specific improvements
- Rewritten bullet points
```

---

## 6. 📊 Scoring System (`analyzer/scorer.py`)

### Metrics:

* Skills match → 40%
* Experience → 30%
* Projects → 20%
* ATS format → 10%

```python
final_score = (skills*0.4 + exp*0.3 + projects*0.2 + ats*0.1)
```

---

## 7. 🌐 Backend API (`main.py`)

### Endpoints:

#### POST `/analyze`

* Input:

  * Resume file
  * Job role / description

* Output:

  * Score
  * Missing skills
  * AI feedback

---

## 8. 💻 Frontend (React)

### Pages:

* Upload Resume
* Enter Job Role
* Results Dashboard

### Components:

* Score Card
* Skills Match Chart
* Suggestions Panel

---

# 📁 Project Structure

```text
ai-resume-analyzer/
│
├── backend/
│   ├── parser/
│   ├── analyzer/
│   │   ├── skills.py
│   │   ├── matcher.py
│   │   ├── gap.py
│   │   └── scorer.py
│   ├── ai_engine/
│   └── main.py
│
├── frontend/
│   ├── components/
│   ├── pages/
│   └── utils/
│
├── data/
│   └── skills_db.json
│
└── plan.md
```

---

# ⚙️ Development Phases

## Phase 1: Setup

* Setup FastAPI backend
* Setup React frontend
* Create basic upload API

---

## Phase 2: Resume Parsing

* Extract text from PDF
* Return raw content

---

## Phase 3: Skill Matching

* Build skills DB
* Implement matching logic

---

## Phase 4: Scoring System

* Calculate match score
* Display breakdown

---

## Phase 5: AI Integration

* Connect LLM API
* Generate structured feedback

---

## Phase 6: UI Dashboard

* Show:

  * Score
  * Missing skills
  * Suggestions

---

## Phase 7: Demo Optimization

* Add sample resumes
* Improve response speed
* Polish UI

---

# 🧪 Testing Plan

* Test with:

  * Good resume
  * Weak resume
* Validate:

  * Skill detection
  * Score accuracy
  * AI output quality

---

# 🎤 Demo Flow (IMPORTANT)

1. Upload weak resume
2. Select role (e.g., Web Developer)
3. Show:

   * Low score
   * Missing skills
4. Show AI suggestions
5. Show improved version

---

# 🏆 Winning Features (Focus)

* Job-role based analysis
* Skill gap → action plan
* AI rewrite

---

# ⚠️ Risks

| Risk           | Solution          |
| -------------- | ----------------- |
| Bad parsing    | Use clean resumes |
| Weak AI output | Tune prompt       |
| Time limit     | Focus on MVP      |

---

# 🚀 MVP Checklist

* [ ] Resume upload
* [ ] Text extraction
* [ ] Skill detection
* [ ] Match score
* [ ] AI feedback
* [ ] Basic UI

---

# 🔥 Final Pitch

> “An AI-powered career coach that analyzes resumes, identifies gaps, and tells users exactly how to get hired.”

---

**Build fast. Keep it sharp. Focus on demo.**

import React, { useMemo, useState } from "react";
import { createRoot } from "react-dom/client";
import { AlertCircle, CheckCircle2, FileText, Loader2, Upload } from "lucide-react";
import "./styles.css";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

function App() {
  const [file, setFile] = useState(null);
  const [jobRole, setJobRole] = useState("Frontend Developer");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  async function handleSubmit(event) {
    event.preventDefault();
    setError("");
    setResult(null);

    if (!file) {
      setError("Upload a PDF, DOCX, or TXT resume first.");
      return;
    }

    const formData = new FormData();
    formData.append("resume", file);
    formData.append("job_role", jobRole);

    setIsLoading(true);
    try {
      const response = await fetch(`${API_URL}/analyze`, {
        method: "POST",
        body: formData,
      });
      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.detail || "Resume analysis failed.");
      }
      setResult(data);
    } catch (fetchError) {
      setError(fetchError.message);
    } finally {
      setIsLoading(false);
    }
  }

  const scoreTone = useMemo(() => {
    const score = result?.score?.overall ?? 0;
    if (score >= 75) return "text-emerald-700";
    if (score >= 50) return "text-amber-700";
    return "text-rose-700";
  }, [result]);

  return (
    <main className="min-h-screen bg-[#f6f7f9] text-slate-950">
      <section className="border-b border-slate-200 bg-white">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-5 py-5">
          <div>
            <h1 className="text-2xl font-semibold tracking-normal">AI Resume Analyzer</h1>
            <p className="mt-1 text-sm text-slate-600">Upload, match, score, and improve a resume for a target role.</p>
          </div>
          <div className="hidden rounded-md border border-slate-200 px-3 py-2 text-sm text-slate-600 sm:block">
            MVP dashboard
          </div>
        </div>
      </section>

      <div className="mx-auto grid max-w-6xl gap-6 px-5 py-6 lg:grid-cols-[380px_1fr]">
        <form onSubmit={handleSubmit} className="space-y-5 rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
          <div>
            <label className="text-sm font-medium text-slate-800" htmlFor="resume">
              Resume file
            </label>
            <label className="mt-2 flex min-h-36 cursor-pointer flex-col items-center justify-center rounded-md border border-dashed border-slate-300 bg-slate-50 px-4 text-center hover:border-slate-500">
              <Upload className="mb-3 h-6 w-6 text-slate-500" aria-hidden="true" />
              <span className="text-sm font-medium text-slate-800">{file ? file.name : "Choose PDF, DOCX, or TXT"}</span>
              <span className="mt-1 text-xs text-slate-500">The file is sent only to your local backend.</span>
              <input
                id="resume"
                className="sr-only"
                type="file"
                accept=".pdf,.docx,.txt"
                onChange={(event) => setFile(event.target.files?.[0] || null)}
              />
            </label>
          </div>

          <div>
            <label className="text-sm font-medium text-slate-800" htmlFor="job-role">
              Job role or description
            </label>
            <textarea
              id="job-role"
              value={jobRole}
              onChange={(event) => setJobRole(event.target.value)}
              className="mt-2 min-h-32 w-full rounded-md border border-slate-300 bg-white px-3 py-2 text-sm outline-none focus:border-slate-700 focus:ring-2 focus:ring-slate-200"
              placeholder="Paste a role, job description, or required skills."
            />
          </div>

          {error && (
            <div className="flex gap-2 rounded-md border border-rose-200 bg-rose-50 p-3 text-sm text-rose-800">
              <AlertCircle className="h-5 w-5 shrink-0" aria-hidden="true" />
              <span>{error}</span>
            </div>
          )}

          <button
            type="submit"
            disabled={isLoading}
            className="inline-flex h-11 w-full items-center justify-center gap-2 rounded-md bg-slate-950 px-4 text-sm font-semibold text-white hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-60"
          >
            {isLoading ? <Loader2 className="h-4 w-4 animate-spin" aria-hidden="true" /> : <FileText className="h-4 w-4" aria-hidden="true" />}
            Analyze resume
          </button>
        </form>

        <section className="space-y-6">
          {!result ? <EmptyState /> : <Results result={result} scoreTone={scoreTone} />}
        </section>
      </div>
    </main>
  );
}

function EmptyState() {
  return (
    <div className="flex min-h-[440px] items-center justify-center rounded-lg border border-slate-200 bg-white p-8 text-center shadow-sm">
      <div>
        <FileText className="mx-auto h-10 w-10 text-slate-400" aria-hidden="true" />
        <h2 className="mt-4 text-lg font-semibold">Results dashboard</h2>
        <p className="mt-2 max-w-md text-sm leading-6 text-slate-600">
          Run an analysis to see the resume score, skill coverage, missing skills, weak sections, and improvement suggestions.
        </p>
      </div>
    </div>
  );
}

function Results({ result, scoreTone }) {
  return (
    <>
      <div className="grid gap-4 md:grid-cols-4">
        <Metric label="Overall" value={`${result.score.overall}%`} tone={scoreTone} />
        <Metric label="Skills" value={`${result.score.breakdown.skills}%`} />
        <Metric label="Experience" value={`${result.score.breakdown.experience}%`} />
        <Metric label="ATS" value={`${result.score.breakdown.ats_format}%`} />
      </div>

      <div className="grid gap-6 xl:grid-cols-2">
        <Panel title="Matched skills">
          <SkillList skills={result.matched_skills} variant="matched" empty="No required skills matched yet." />
        </Panel>
        <Panel title="Missing skills">
          <SkillList skills={result.missing_skills} variant="missing" empty="No missing skills detected." />
        </Panel>
      </div>

      <Panel title="Feedback">
        <FeedbackBlock title="Strengths" items={result.feedback.strengths} icon="success" />
        <FeedbackBlock title="Weaknesses" items={result.feedback.weaknesses} />
        <FeedbackBlock title="Improvements" items={result.feedback.improvements} />
      </Panel>

      <Panel title="Resume preview">
        <p className="max-h-44 overflow-auto whitespace-pre-wrap text-sm leading-6 text-slate-700">{result.resume_preview}</p>
      </Panel>
    </>
  );
}

function Metric({ label, value, tone = "text-slate-950" }) {
  return (
    <div className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
      <p className="text-xs font-medium uppercase tracking-normal text-slate-500">{label}</p>
      <p className={`mt-2 text-3xl font-semibold ${tone}`}>{value}</p>
    </div>
  );
}

function Panel({ title, children }) {
  return (
    <div className="rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
      <h2 className="text-base font-semibold text-slate-900">{title}</h2>
      <div className="mt-4 space-y-4">{children}</div>
    </div>
  );
}

function SkillList({ skills, variant, empty }) {
  if (!skills?.length) {
    return <p className="text-sm text-slate-500">{empty}</p>;
  }

  const className =
    variant === "matched"
      ? "border-emerald-200 bg-emerald-50 text-emerald-800"
      : "border-amber-200 bg-amber-50 text-amber-800";

  return (
    <div className="flex flex-wrap gap-2">
      {skills.map((skill) => (
        <span key={skill} className={`rounded-md border px-2.5 py-1 text-sm ${className}`}>
          {skill}
        </span>
      ))}
    </div>
  );
}

function FeedbackBlock({ title, items, icon }) {
  return (
    <div>
      <h3 className="mb-2 text-sm font-semibold text-slate-800">{title}</h3>
      <ul className="space-y-2">
        {items.map((item) => (
          <li key={item} className="flex gap-2 text-sm leading-6 text-slate-700">
            {icon === "success" ? (
              <CheckCircle2 className="mt-0.5 h-4 w-4 shrink-0 text-emerald-600" aria-hidden="true" />
            ) : (
              <span className="mt-2 h-1.5 w-1.5 shrink-0 rounded-full bg-slate-400" />
            )}
            <span>{item}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}

createRoot(document.getElementById("root")).render(<App />);


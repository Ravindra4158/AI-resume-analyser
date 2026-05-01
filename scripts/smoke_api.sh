#!/usr/bin/env bash
set -euo pipefail

API_URL="${API_URL:-http://127.0.0.1:8000}"
RESUME_FILE="${1:-samples/strong_frontend_resume.txt}"
JOB_ROLE="${2:-Frontend Developer React JavaScript TypeScript HTML CSS Tailwind API Git GitHub}"

echo "Checking backend health at ${API_URL}/health"
curl --fail --silent "${API_URL}/health"
echo

echo "Analyzing ${RESUME_FILE}"
curl --fail --silent \
  -X POST "${API_URL}/analyze" \
  -F "resume=@${RESUME_FILE}" \
  -F "job_role=${JOB_ROLE}"
echo

from __future__ import annotations

import re
from io import BytesIO
from pathlib import Path

import pdfplumber
from docx import Document


SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".txt"}


class UnsupportedResumeFormat(ValueError):
    """Raised when a resume file type cannot be parsed."""


def normalize_text(text: str) -> str:
    text = text.replace("\x00", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def parse_resume(filename: str, content: bytes) -> str:
    extension = Path(filename).suffix.lower()

    if extension not in SUPPORTED_EXTENSIONS:
        raise UnsupportedResumeFormat(
            "Please upload a PDF, DOCX, or TXT resume."
        )

    if extension == ".pdf":
        text = _parse_pdf(content)
    elif extension == ".docx":
        text = _parse_docx(content)
    else:
        text = content.decode("utf-8", errors="ignore")

    return normalize_text(text)


def _parse_pdf(content: bytes) -> str:
    pages: list[str] = []
    with pdfplumber.open(BytesIO(content)) as pdf:
        for page in pdf.pages:
            pages.append(page.extract_text() or "")
    return "\n".join(pages)


def _parse_docx(content: bytes) -> str:
    document = Document(BytesIO(content))
    return "\n".join(paragraph.text for paragraph in document.paragraphs)


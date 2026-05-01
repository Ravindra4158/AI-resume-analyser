from __future__ import annotations

import os
from dataclasses import dataclass, field

from dotenv import find_dotenv, load_dotenv


load_dotenv(find_dotenv(), override=False)


def _csv_env(name: str, default: str) -> list[str]:
    value = os.getenv(name, default)
    return [item.strip() for item in value.split(",") if item.strip()]


def _first_env(*names: str, default: str = "") -> str:
    for name in names:
        value = os.getenv(name, "").strip()
        if value:
            return value
    return default


@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv("APP_NAME", "AI Resume Analyzer")
    app_version: str = os.getenv("APP_VERSION", "1.0.0")
    environment: str = os.getenv("ENVIRONMENT", "development")
    allowed_origins: list[str] = field(
        default_factory=lambda: _csv_env(
            "ALLOWED_ORIGINS",
            "http://localhost:5173,http://127.0.0.1:5173,http://0.0.0.0:5173",
        )
    )
    max_upload_bytes: int = int(os.getenv("MAX_UPLOAD_BYTES", str(5 * 1024 * 1024)))
    resume_preview_chars: int = int(os.getenv("RESUME_PREVIEW_CHARS", "800"))
    llm_api_key: str = _first_env("GEMINI_API_KEY", "OPENAI_API_KEY")
    llm_model: str = _first_env("GEMINI_MODEL", "OPENAI_MODEL", default="gemini-1.5-pro")
    llm_base_url: str = _first_env(
        "GEMINI_BASE_URL",
        "OPENAI_BASE_URL",
        default="https://generativelanguage.googleapis.com/v1beta/openai/",
    )
    llm_timeout_seconds: int = int(_first_env("GEMINI_TIMEOUT_SECONDS", "OPENAI_TIMEOUT_SECONDS", default="25"))


settings = Settings()

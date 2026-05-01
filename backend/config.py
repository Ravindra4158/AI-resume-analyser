from __future__ import annotations

import os
from dataclasses import dataclass, field


def _csv_env(name: str, default: str) -> list[str]:
    value = os.getenv(name, default)
    return [item.strip() for item in value.split(",") if item.strip()]


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


settings = Settings()

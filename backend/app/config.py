import os

from functools import lru_cache
from pathlib import Path

from pydantic import BaseModel, Field, EmailStr


ENV_FILE_PATH = Path(__file__).resolve().parents[2] / ".env"
DEFAULT_TRUSTED_ORIGINS: tuple[str, ...] = ("http://localhost:5173",)


def _load_env_file() -> None:
    if not ENV_FILE_PATH.exists():
        return

    for line in ENV_FILE_PATH.read_text().splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        if key and key not in os.environ:
            os.environ[key] = value


def _persist_env_var(key: str, value: str) -> None:
    lines: list[str]
    if ENV_FILE_PATH.exists():
        lines = ENV_FILE_PATH.read_text().splitlines()
    else:
        ENV_FILE_PATH.touch()
        lines = []

    updated = False
    new_lines: list[str] = []
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            new_lines.append(line)
            continue

        current_key, _, _ = line.partition("=")
        if current_key.strip() == key and not updated:
            new_lines.append(f"{key}={value}")
            updated = True
        else:
            new_lines.append(line)

    if not updated:
        if new_lines and new_lines[-1].strip() != "":
            new_lines.append("")
        new_lines.append(f"{key}={value}")

    ENV_FILE_PATH.write_text("\n".join(new_lines) + "\n")


_load_env_file()


class EmailSettings(BaseModel):
    provider: str = Field(default="smtp", description="Email provider identifier")
    smtp_host: str | None = Field(default=None, description="SMTP server host")
    smtp_port: int = Field(default=587, description="SMTP server port")
    smtp_username: str | None = None
    smtp_password: str | None = None
    sendgrid_api_key: str | None = Field(default=None, description="SendGrid API key")
    default_sender: EmailStr | None = None

    def missing_fields(self) -> list[str]:
        if self.provider.lower() != "smtp":
            return []

        missing: list[str] = []
        if not self.smtp_host:
            missing.append("smtp_host")
        if not self.smtp_username:
            missing.append("smtp_username")
        if not self.smtp_password:
            missing.append("smtp_password")
        if not self.default_sender:
            missing.append("default_sender")
        if not self.smtp_port:
            missing.append("smtp_port")
        return missing

    @property
    def is_configured(self) -> bool:
        return len(self.missing_fields()) == 0


class AppSettings(BaseModel):
    target_email: EmailStr | None = Field(default=None, description="Default report recipient")
    app_base_url: str = Field(default="http://localhost:8000", description="Base URL for report links")
    store_transcripts: bool = Field(default=True, description="Whether to persist transcripts in memory")
    secret_token: str = Field(..., description="Simple bearer token for auth")
    report_language: str = Field(default="en", description="Report language code")
    trusted_origins: tuple[str, ...] = Field(
        default=DEFAULT_TRUSTED_ORIGINS,
        description="Origins permitted to access the API via CORS",
    )
    email: EmailSettings = Field(default_factory=EmailSettings)
    gpt5_api_key: str | None = Field(default=None, description="API key for GPT-5 evaluation")
    gpt5_api_base_url: str = Field(default="https://api.openai.com/v1", description="Base URL for GPT-5 compatible APIs")
    gpt5_model: str = Field(default="gpt-5", description="Model identifier to request for GPT-5 evaluations")
    gpt5_temperature: float | None = Field(
        default=None,
        description="Optional sampling temperature for GPT-5 evaluations; omit to use API default.",
    )

    @staticmethod
    def from_env() -> "AppSettings":
        return AppSettings(
            target_email=os.getenv("TARGET_EMAIL"),
            app_base_url=_load_app_base_url(),
            store_transcripts=os.getenv("STORE_TRANSCRIPTS", "true").lower() == "true",
            secret_token=_load_secret_token(),
            report_language=os.getenv("REPORT_LANGUAGE", "en"),
            trusted_origins=_load_trusted_origins(),
            email=EmailSettings(
                provider=os.getenv("EMAIL_PROVIDER", "smtp"),
                smtp_host=os.getenv("SMTP_HOST"),
                smtp_port=int(os.getenv("SMTP_PORT", "587")),
                smtp_username=os.getenv("SMTP_USERNAME"),
                smtp_password=os.getenv("SMTP_PASSWORD"),
                sendgrid_api_key=os.getenv("SENDGRID_API_KEY"),
                default_sender=os.getenv("EMAIL_DEFAULT_SENDER", os.getenv("TARGET_EMAIL")),
            ),
            gpt5_api_key=os.getenv("GPT5_API_KEY"),
            gpt5_api_base_url=os.getenv("GPT5_API_BASE_URL", "https://api.openai.com/v1"),
            gpt5_model=os.getenv("GPT5_MODEL", "gpt-5"),
            gpt5_temperature=_load_temperature(),
        )


def _load_app_base_url() -> str:
    """
    Load the application base URL with automatic Render deployment support.

    Priority:
    1. APP_BASE_URL (if explicitly set)
    2. RENDER_EXTERNAL_URL (automatically set by Render)
    3. http://localhost:8000 (local development fallback)
    """
    # Check if explicitly configured
    app_url = os.getenv("APP_BASE_URL")
    if app_url and app_url.strip():
        return app_url.strip()

    # Use Render's auto-generated URL (available in Render deployments)
    render_url = os.getenv("RENDER_EXTERNAL_URL")
    if render_url and render_url.strip():
        return render_url.strip()

    # Fallback to local development
    return "http://localhost:8000"


def _load_secret_token() -> str:
    token = os.getenv("APP_SECRET_TOKEN")
    if token is None or token.strip() == "":
        raise ValueError(
            "APP_SECRET_TOKEN must be set to a strong, non-empty value before starting the application."
        )

    token = token.strip()
    if token.lower() == "dev-secret" or len(token) < 32:
        raise ValueError("APP_SECRET_TOKEN must be at least 32 characters and not use the insecure default.")

    return token


def _load_temperature() -> float | None:
    raw = os.getenv("GPT5_TEMPERATURE")
    if raw is None or raw.strip() == "":
        return None

    try:
        return float(raw)
    except ValueError as exc:  # pragma: no cover - config error surfaced during startup
        raise ValueError("GPT5_TEMPERATURE must be a numeric value") from exc


def _load_trusted_origins() -> tuple[str, ...]:
    """
    Load trusted CORS origins with automatic Render deployment support.

    Automatically includes RENDER_EXTERNAL_URL if present (for Render deployments).
    """
    raw = os.getenv("APP_TRUSTED_ORIGINS")

    # Start with explicitly configured origins or defaults
    if raw and raw.strip():
        origins = [origin.strip() for origin in raw.split(",") if origin.strip()]
    else:
        origins = list(DEFAULT_TRUSTED_ORIGINS)

    # Add Render's external URL if available and not already included
    render_url = os.getenv("RENDER_EXTERNAL_URL")
    if render_url and render_url.strip():
        render_url = render_url.strip()
        if render_url not in origins:
            origins.append(render_url)

    return tuple(origins) if origins else DEFAULT_TRUSTED_ORIGINS


@lru_cache(maxsize=1)
def get_settings() -> AppSettings:
    return AppSettings.from_env()


def set_gpt5_api_key(api_key: str) -> AppSettings:
    os.environ["GPT5_API_KEY"] = api_key
    get_settings.cache_clear()
    return get_settings()


def set_email_settings(**kwargs: str | int | None) -> AppSettings:
    env_mapping = {
        "provider": "EMAIL_PROVIDER",
        "smtp_host": "SMTP_HOST",
        "smtp_port": "SMTP_PORT",
        "smtp_username": "SMTP_USERNAME",
        "smtp_password": "SMTP_PASSWORD",
        "default_sender": "EMAIL_DEFAULT_SENDER",
        "target_email": "TARGET_EMAIL",
    }

    updated = False
    for key, value in kwargs.items():
        if key not in env_mapping or value in (None, ""):
            continue
        env_key = env_mapping[key]
        os.environ[env_key] = str(value)
        updated = True

    if updated:
        get_settings.cache_clear()

    return get_settings()

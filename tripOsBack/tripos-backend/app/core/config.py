from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "TripOS API"
    API_V1_PREFIX: str = "/api/v1"
    CORS_ORIGINS: list[str] = Field(default_factory=list)

    DATABASE_URL: str = (
        "postgresql+psycopg://tripos_user:Sovan13022008@localhost:5432/TripOs"
    )

    JWT_SECRET_KEY: str = "replace-this-with-a-long-random-secret"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    ADMIN_EMAILS: str = ""
    OPENAI_API_KEY: str | None = None
    OPENAI_BASE_URL: str = "https://api.openai.com/v1"
    OPENAI_MODEL: str = "gpt-4o-mini"
    UPLOAD_DIR: Path = Path("uploads")

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parents[2] / ".env",
        extra="ignore",
    )


    @property
    def admin_emails(self) -> set[str]:
        return {
            email.strip().casefold()
            for email in self.ADMIN_EMAILS.split(",")
            if email.strip()
        }


settings = Settings()

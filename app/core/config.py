from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuración leída desde variables de entorno / archivo .env"""

    DATABASE_URL: str = "sqlite:///./blog.db"
    DB_ECHO: bool = False

    # El secreto es la llave maestra de la API: en producción SIEMPRE desde .env
    JWT_SECRET: str = "change-me-in-prod"
    JWT_ALG: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    MAX_UPLOAD_MB: int = 3

    @field_validator("DATABASE_URL")
    @classmethod
    def normalize_db_url(cls, value: str) -> str:
        # Render (y otros proveedores) entregan "postgres://" o "postgresql://".
        # SQLAlchemy 2.1 usa por defecto el driver psycopg (v3), pero en
        # requirements.txt tenemos psycopg2-binary: lo indicamos explícitamente.
        for prefix in ("postgres://", "postgresql://"):
            if value.startswith(prefix):
                return "postgresql+psycopg2://" + value[len(prefix):]
        return value

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()

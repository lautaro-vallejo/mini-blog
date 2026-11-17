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

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()

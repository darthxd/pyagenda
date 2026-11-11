from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    APP_NAME: str = "pyagenda"
    APP_DESCRIPTION: str = "backend para projeto agenda pi-ii"
    APP_VERSION: str = "1.0.0"
    PORT: int = 8080
    DEBUG: bool = False

    JWT_SECRET: str = "tokennaomuitosecreto"
    DB_PATH: str = "sqlite:///app.db"
    ALLOWED_ORIGINS: list[str] = ["*"]

    @property
    def split_allowed_origins(self) -> str:
        return ", ".join(self.ALLOWED_ORIGINS)

config = Config()

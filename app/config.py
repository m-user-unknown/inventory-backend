from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Central app configuration, loaded from environment variables / .env file.
    Override any of these via a .env file in the project root or real env vars.
    """
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Database
    # Individual PostgreSQL parts (used to build database_url below if you don't
    # want to set DATABASE_URL directly). Override via env vars / .env file.
    postgres_user: str = "inventory_user"
    postgres_password: str = "admin"
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "inventory_db"

    # Full connection string. If DATABASE_URL is set in the environment, it wins.
    # Otherwise it's built from the postgres_* fields above.
    database_url: str = ""

    def build_database_url(self) -> str:
        if self.database_url:
            return self.database_url
        return (
            f"postgresql+psycopg2://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    # JWT / auth
    secret_key: str = "55dc66f6902ad1a6fe23a22506c41761c186c6dc8e978cb9109f5a38382dc667"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 8  # 8 hours

    # App metadata
    app_name: str = "Inventory Management API"
    app_version: str = "1.0.0"

    # Business rules
    default_low_stock_threshold: int = 10


settings = Settings()

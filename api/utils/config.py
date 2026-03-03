import os
from dotenv import load_dotenv
from pathlib import Path

# Get current file path
BASE_DIR = Path(__file__).resolve().parent

PARENT_DIR = BASE_DIR.parent

# Load .env from parent folder
env_path = PARENT_DIR / ".env"
load_dotenv(dotenv_path=env_path)


class Settings:
    PROJECT_NAME: str = "Invitely"
    PROJECT_VERSION: str = "1.0.0"

    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", 5432)
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "tdd")

    DATABASE_URL = (
        f"postgresql://{POSTGRES_USER}:"
        f"{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:"
        f"{POSTGRES_PORT}/{POSTGRES_DB}"
    )


settings = Settings()
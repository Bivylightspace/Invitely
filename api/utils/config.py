from pathlib import Path

from decouple import config
from pydantic_settings import BaseSettings

# Use this to build paths inside the project
BASE_DIR = Path(__file__).resolve().parent


class Settings(BaseSettings):
    """Class to hold application's config values."""
    
    # Application configurations
    APP_NAME: str = config("APP_NAME", default="Invitey API")
    APP_VERSION: str = config("APP_VERSION", default="0.1.0")
    APP_DESCRIPTION: str = config("APP_DESCRIPTION", default="Invitey API")
    ENVIRONMENT: str = config("ENVIRONMENT", default="production")
    LOG_LEVEL: str = config("LOG_LEVEL", default="INFO")
    
    # Security configurations
    JWT_SECRET_KEY: str = config("JWT_SECRET_KEY", default="")
    JWT_ALGORITHM: str = config("JWT_ALGORITHM", default="HS256")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = config(
        "JWT_ACCESS_TOKEN_EXPIRE_MINUTES", default=15
    )
    JWT_REFRESH_TOKEN_EXPIRE_MINUTES: int = config(
        "JWT_REFRESH_TOKEN_EXPIRE_MINUTES", default=30)

    # Database configurations
    DB_HOST: str = config("DB_HOST", default="localhost")
    DB_PORT: int = config("DB_PORT", default=5432)
    DB_USER: str = config("DB_USER", default="postgres")
    DB_PASSWORD: str = config("DB_PASSWORD", default="postgres")
    DB_NAME: str = config("DB_NAME", default="postgres")
    DB_TYPE: str = config("DB_TYPE", default="postgresql")
    DB_ECHO: bool = config("DB_ECHO", default=False)
    # Connection pool settings
    DB_POOL_SIZE: int = config("DB_POOL_SIZE", default=5, cast=int)
    DB_MAX_OVERFLOW: int = config("DB_MAX_OVERFLOW", default=10, cast=int)
    DB_POOL_PRE_PING: bool = config("DB_POOL_PRE_PING", default=True, cast=bool)

    # SendGrid configurations
    SENDGRID_API_KEY: str = config("SENDGRID_API_KEY", default="")
    SENDER_EMAIL: str = config("SENDER_EMAIL", default="")

    REDIS_HOST: str = config("REDIS_HOST", default="157.180.27.189")
    REDIS_PORT: int = config("REDIS_PORT", default="6379", cast=int)
    REDIS_PASSWORD: str = config("REDIS_PASSWORD", default="Njhdhj")
    REDIS_DB: int = config("REDIS_DB", default="0", cast=int)
    REDIS_QUEUE: str = config("REDIS_QUEUE", default="default")

    # Email configurations
    EMAIL_USERNAME: str = config("EMAIL_USERNAME", default="dummy@gmail.com")
    EMAIL_PASSWORD: str = config("EMAIL_PASSWORD", default="dummy_password")
    EMAIL_FROM: str = config("EMAIL_FROM", default="dummy@gmail.com")
    EMAIL_PORT: int = config("EMAIL_PORT", default=587)
    EMAIL_HOST: str = config("EMAIL_HOST", default="dummy_host.com")

    # Frontend URL
    FRONTEND_URL: str = config("FRONTEND_URL", default="")
    COOKIE_DOMAIN: str = config("COOKIE_DOMAIN", default="")
    FLUTTERWAVE_SECRET_KEY: str = config("FLUTTERWAVE_SECRET_KEY", default="")
    FLUTTERWAVE_SUCCESS_URL: str = config("FLUTTERWAVE_SUCCESS_URL", default="")
    FLUTTERWAVE_CANCEL_URL: str = config("FLUTTERWAVE_CANCEL_URL", default="")
   

    # Google authentication credentials
    GOOGLE_CLIENT_ID: str = config("GOOGLE_CLIENT_ID", default="")
    GOOGLE_CLIENT_SECRET: str = config("GOOGLE_CLIENT_SECRET", default="")
    GOOGLE_REDIRECT_URI: str = config("GOOGLE_REDIRECT_URI", default="")
    GOOGLE_CONF_URL: str = config("GOOGLE_CONF_URL", default="")
    GOOGLE_REDIRECT_FRONTEND_URL: str = config(
        "GOOGLE_REDIRECT_FRONTEND_URL", default="")


settings = Settings()
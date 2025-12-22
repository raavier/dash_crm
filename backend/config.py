"""
Configuration settings for the Dashboard CRM API.
Loads environment variables and provides configuration classes.
"""
from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Databricks connection (managed by databricks-sdk Config)
    databricks_host: str

    # API settings
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    # Frontend URL for CORS
    frontend_url: str = "http://localhost:5175"

    # Database catalog and schema
    catalog: str = "hs_franquia"
    schema_gold: str = "gold_connect_bot"
    schema_silver: str = "silver_crm"

    # Cache settings
    cache_enabled: bool = True
    cache_ttl: int = 14400  # 4 hours in seconds
    cache_maxsize: int = 1000  # Maximum number of cached items

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        # Don't fail if .env file doesn't exist (Databricks Apps uses env vars directly)
        extra = "ignore"


# Global settings instance
settings = Settings()

# Note: Token management is now handled by databricks.sdk.core.Config
# in database.py using credentials_provider for auto-renewing tokens

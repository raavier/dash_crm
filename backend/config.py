"""
Configuration settings for the Dashboard CRM API.
Loads environment variables and provides configuration classes.
"""
from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Databricks connection
    databricks_host: str
    databricks_http_path: str
    databricks_token: str = ""  # Will be set after initialization

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

# Token cache
_token_cache = None

def get_token() -> str:
    """
    Get Databricks token from environment variable.

    The token is automatically injected by Databricks Apps from the
    configured secret resource (resource key: 'secret').
    """
    global _token_cache

    if _token_cache is not None:
        return _token_cache

    # Token is injected by Databricks Apps from secret resource
    env_token = os.getenv("DATABRICKS_TOKEN", "")
    if env_token:
        _token_cache = env_token
        settings.databricks_token = env_token
        return env_token

    # If no token found, return empty (will fail on first query)
    print("Warning: DATABRICKS_TOKEN environment variable not set")
    return ""

"""
Configuration settings for the Dashboard CRM API.
Loads environment variables and provides configuration classes.
"""
from pydantic_settings import BaseSettings
from typing import Optional
import os


def get_databricks_token_from_secrets() -> Optional[str]:
    """
    Get Databricks token from secrets using REST API.

    In Databricks Apps, we need to use the REST API to access secrets,
    not dbutils (which requires Spark and is not available in Apps).

    This requires the app to have permission to read from the secret scope.
    """
    try:
        import httpx

        # Get the workspace host from environment
        host = os.getenv("DATABRICKS_HOST")
        if not host:
            return None

        # Try to get token using Databricks Apps service principal
        # In Apps, there should be a DATABRICKS_TOKEN env var automatically set
        service_token = os.getenv("DATABRICKS_TOKEN")
        if not service_token:
            return None

        # Use REST API to get secret
        url = f"https://{host}/api/2.0/secrets/get"
        headers = {"Authorization": f"Bearer {service_token}"}
        params = {
            "scope": "connectdata-kv-prd",
            "key": "cnx-databricks-hs-community"
        }

        response = httpx.get(url, headers=headers, params=params, timeout=10.0)
        if response.status_code == 200:
            return response.json().get("value")

        return None
    except Exception as e:
        print(f"Debug: Failed to get token from secrets API: {e}")
        return None


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

# Token cache to avoid multiple dbutils calls
_token_cache = None

def get_token() -> str:
    """
    Get Databricks token lazily.
    This function is called instead of accessing settings.databricks_token directly.
    It fetches the token on first use to avoid import errors at startup.

    Priority order:
    1. Cached token (from previous call)
    2. Environment variable DATABRICKS_TOKEN
    3. Secrets API (if running in Databricks Apps with service principal)
    """
    global _token_cache

    if _token_cache is not None:
        return _token_cache

    print("Debug: get_token() called, attempting to fetch token...")

    # Try to get from environment variable first (most reliable)
    env_token = os.getenv("DATABRICKS_TOKEN")
    if env_token:
        print("Debug: Token found in DATABRICKS_TOKEN environment variable")
        _token_cache = env_token
        settings.databricks_token = env_token
        return env_token

    # Try to get from secrets API (for Apps with service principal)
    secrets_token = get_databricks_token_from_secrets()
    if secrets_token:
        print("Debug: Token retrieved from Databricks Secrets API")
        _token_cache = secrets_token
        settings.databricks_token = secrets_token
        return secrets_token

    # Fallback to empty string (will fail when actually trying to connect)
    print("Warning: No Databricks token found. Queries will fail.")
    return ""

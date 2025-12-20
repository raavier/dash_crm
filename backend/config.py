"""
Configuration settings for the Dashboard CRM API.
Loads environment variables and provides configuration classes.
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Databricks connection
    databricks_host: str
    databricks_http_path: str
    databricks_token: str

    # API settings
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    # Frontend URL for CORS
    frontend_url: str = "http://localhost:5175"

    # Database catalog and schema
    catalog: str = "hs_franquia"
    schema_gold: str = "gold_connect_bot"
    schema_silver: str = "silver_crm"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = Settings()

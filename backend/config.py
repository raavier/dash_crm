"""
Configuration settings for the Dashboard CRM API.
Loads environment variables and provides configuration classes.
"""
from pydantic_settings import BaseSettings
from typing import Optional
import os


def get_databricks_token() -> str:
    """
    Get Databricks token from secrets or environment variable.
    In production (Databricks Apps), uses dbutils.secrets.get().
    In development, uses environment variable.
    """
    try:
        # Try to import dbutils (available in Databricks runtime)
        from pyspark.dbutils import DBUtils
        from pyspark.sql import SparkSession

        spark = SparkSession.builder.getOrCreate()
        dbutils = DBUtils(spark)

        # Get token from secret scope
        token = dbutils.secrets.get(scope="connectdata-kv-prd", key="cnx-databricks-hs-community")
        return token
    except ImportError:
        # Running locally, use environment variable
        token = os.getenv("DATABRICKS_TOKEN")
        if not token:
            raise ValueError("DATABRICKS_TOKEN not found in environment variables")
        return token


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


# Global settings instance
settings = Settings()

# Initialize Databricks token (from secrets or env var)
try:
    settings.databricks_token = get_databricks_token()
except Exception as e:
    # If we can't get the token, try from env (fallback)
    print(f"Warning: Could not get token from dbutils: {e}")
    if not settings.databricks_token:
        settings.databricks_token = os.getenv("DATABRICKS_TOKEN", "")

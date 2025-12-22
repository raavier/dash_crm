"""
Databricks SQL connection management.
Follows official Databricks template pattern for auth and connection management.
"""
from databricks.sdk.core import Config
from databricks import sql
from typing import List, Dict, Any, Optional
from contextlib import contextmanager
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DatabricksConnection:
    """Manages Databricks SQL connections using official SDK pattern."""

    def __init__(self):
        """
        Initialize connection using Databricks SDK Config.

        Config auto-detects authentication from:
        - Environment variables (DATABRICKS_HOST, DATABRICKS_TOKEN, etc.)
        - Databricks Apps managed auth
        - .databrickscfg file
        """
        try:
            # Use SDK Config (auto-detects env vars and auth)
            self.cfg = Config()
            self.warehouse_id = os.getenv('DATABRICKS_WAREHOUSE_ID')

            if not self.warehouse_id:
                raise ValueError(
                    "DATABRICKS_WAREHOUSE_ID environment variable must be set. "
                    "Check app.yaml configuration."
                )

            logger.info(f"Initialized Databricks connection - Warehouse: {self.warehouse_id}")
        except Exception as e:
            logger.error(f"Failed to initialize Databricks connection: {str(e)}")
            raise

    @contextmanager
    def get_connection(self):
        """
        Context manager for Databricks SQL connections.

        Uses credentials_provider for auto-renewing tokens - critical for
        long-running queries that may exceed token expiration time.

        Usage:
            with db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM table")
        """
        connection = None
        try:
            logger.info("Connecting to Databricks SQL Warehouse...")
            connection = sql.connect(
                server_hostname=self.cfg.host,
                http_path=f"/sql/1.0/warehouses/{self.warehouse_id}",
                credentials_provider=lambda: self.cfg.authenticate,
                # Timeout configuration
                _socket_timeout=90,  # 90s socket timeout
                _retry_stop_after_attempts_count=2  # Retry failed requests 2x
            )
            logger.info("Connected to Databricks successfully")
            yield connection
        except Exception as e:
            logger.error(f"Error connecting to Databricks: {str(e)}")
            raise
        finally:
            if connection:
                connection.close()
                logger.info("Databricks connection closed")

    def execute_query(self, query: str, parameters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Execute a SQL query and return results as a list of dictionaries.

        Args:
            query: SQL query string
            parameters: Optional dictionary of query parameters

        Returns:
            List of dictionaries with column names as keys

        Raises:
            Exception: If query execution fails
        """
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    # Execute query with parameters if provided
                    if parameters:
                        cursor.execute(query, parameters)
                    else:
                        cursor.execute(query)

                    # Get column names from cursor description
                    columns = [desc[0] for desc in cursor.description]

                    # Fetch all rows and convert to dictionaries
                    rows = cursor.fetchall()
                    results = [dict(zip(columns, row)) for row in rows]

                    logger.info(f"Query executed successfully. Returned {len(results)} rows")
                    return results

        except Exception as e:
            logger.error(f"Error executing query: {str(e)}")
            logger.error(f"Query: {query[:200]}...")  # Log first 200 chars only
            raise

    def execute_query_single(self, query: str, parameters: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """
        Execute a SQL query and return a single row as a dictionary.

        Args:
            query: SQL query string
            parameters: Optional dictionary of query parameters

        Returns:
            Dictionary with column names as keys, or None if no results
        """
        results = self.execute_query(query, parameters)
        return results[0] if results else None


# Global database instance
db = DatabricksConnection()

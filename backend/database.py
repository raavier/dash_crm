"""
Databricks SQL connection management.
Provides connection pooling and query execution utilities.
"""
from databricks import sql
from typing import List, Dict, Any, Optional
from contextlib import contextmanager
from config import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DatabricksConnection:
    """Manages Databricks SQL connections and query execution."""

    def __init__(self):
        self.server_hostname = settings.databricks_host
        self.http_path = settings.databricks_http_path
        self.access_token = settings.databricks_token

    @contextmanager
    def get_connection(self):
        """
        Context manager for Databricks SQL connections.

        Usage:
            with db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM table")
        """
        connection = None
        try:
            logger.info("Connecting to Databricks...")
            connection = sql.connect(
                server_hostname=self.server_hostname,
                http_path=self.http_path,
                access_token=self.access_token
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
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()

                if parameters:
                    cursor.execute(query, parameters)
                else:
                    cursor.execute(query)

                # Get column names
                columns = [desc[0] for desc in cursor.description]

                # Fetch all rows and convert to dictionaries
                rows = cursor.fetchall()
                results = [dict(zip(columns, row)) for row in rows]

                cursor.close()

                logger.info(f"Query executed successfully. Returned {len(results)} rows")
                return results

        except Exception as e:
            logger.error(f"Error executing query: {str(e)}")
            logger.error(f"Query: {query}")
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

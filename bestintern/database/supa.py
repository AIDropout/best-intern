from typing import Dict, List, Optional, Union

from supabase import Client, create_client

from bestintern.utils.logger import setup_logger
from config.constants import JOB_VECTORS_TABLE, JOBS_TABLE

logger = setup_logger(__name__)


class SupabaseService:
    def __init__(self, url: str, key: str):
        self.client: Client = create_client(url, key)
        logger.info("Connected to Supabase")

    def insert_row(self, table_name: str, data: Dict) -> Optional[Dict]:
        """Insert a row into the specified table."""
        try:
            response = self.client.table(table_name).insert(data).execute()
            if response.status_code == 201:
                logger.info(
                    "Inserted row into table %s with ID: %s",
                    table_name,
                    response.data[0]["id"],
                )
                return response.data[0]
            else:
                logger.error(
                    "Failed to insert row into %s: %d - %s",
                    table_name,
                    response.status_code,
                    response.data,
                )
                return None
        except Exception as e:
            logger.exception(
                "Exception occurred while inserting row into %s: %s", table_name, e
            )
            return None

    def get_rows(
        self,
        table_name: str,
        columns: List[str] = ["*"],
        filters: Optional[Dict[str, Union[str, List[str]]]] = None,
    ) -> Optional[List[Dict]]:
        """Fetch rows from the specified table with optional filters."""
        try:
            query = self.client.table(table_name).select(",".join(columns))
            if filters:
                for key, value in filters.items():
                    if isinstance(value, list):
                        query = query.in_(key, value)
                    else:
                        query = query.eq(key, value)
            response = query.execute()
            if response.status_code == 200:
                logger.info("Fetched rows from table %s", table_name)
                return response.data
            else:
                logger.error(
                    "Failed to fetch rows from %s: %d - %s",
                    table_name,
                    response.status_code,
                    response.data,
                )
                return None
        except Exception as e:
            logger.exception(
                "Exception occurred while fetching rows from %s: %s", table_name, e
            )
            return None

    # Specific Table functions
    def insert_job(self, job_data: Dict) -> Optional[Dict]:
        """Insert a job into the jobs table."""
        return self.insert_row(JOBS_TABLE, job_data)

    def insert_job_vector(self, job_id: str, vector: List[float]) -> Optional[Dict]:
        """Insert a job vector into the job_vectors table."""
        return self.insert_row(JOB_VECTORS_TABLE, {"job_id": job_id, "vector": vector})

    def get_job_vectors(self) -> Optional[List[Dict]]:
        """Fetch all job vectors."""
        return self.get_rows(JOB_VECTORS_TABLE)

    def get_jobs_by_ids(self, job_ids: List[str]) -> Optional[List[Dict]]:
        """Fetch jobs by their IDs."""
        return self.get_rows(JOBS_TABLE, filters={"id": job_ids})

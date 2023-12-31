# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/00_bigquery.ipynb.

# %% auto 0
__all__ = ['logger', 'create_client', 'query_to_dataframe']

# %% ../nbs/00_bigquery.ipynb 3
import logging
import pandas as pd
from google.cloud import bigquery

# %% ../nbs/00_bigquery.ipynb 4
logger = logging.getLogger(__name__)

# %% ../nbs/00_bigquery.ipynb 7
def create_client(
    # key_path: str = None,
    auth_scopes: [str] = [],  # eg: ["bigquery", "drive"]
):
    """Create a BigQuery client with the given auth scopes."""
    if len(auth_scopes) == 0:
        logger.debug("Using default BigQuery client")
        return bigquery.Client()
    else:
        # to pull files from drive or other services, we need to authenticate
        import google.auth
        credentials, project = google.auth.default(
            [f"https://www.googleapis.com/auth/{service}" for service in auth_scopes]
        )
        logger.debug(f"Using BigQuery client with auth scopes: {auth_scopes}")
        return bigquery.Client(
            credentials=credentials,
            project=project,
        )

# %% ../nbs/00_bigquery.ipynb 14
def query_to_dataframe( sql: str, bq_client: bigquery.Client=None) -> pd.DataFrame:
    """
    Query -> DataFrame
    """
    logging.info(f"Querying BigQuery: {sql}")
    if bq_client is None:
        logging.debug("Creating new BigQuery client")
        with bigquery.Client() as bq_client:
            dataframe = bq_client.query(sql).to_dataframe()
    else:
        dataframe = bq_client.query(sql).to_dataframe()

    logging.info(f"dataframe.shape: {dataframe.shape}")
    
    return dataframe

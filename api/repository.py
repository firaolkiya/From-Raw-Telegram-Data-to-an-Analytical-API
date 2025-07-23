from dagster import Definitions
from .dagster_pipeline import telegram_etl_job

defs = Definitions(
    jobs=[telegram_etl_job],
)
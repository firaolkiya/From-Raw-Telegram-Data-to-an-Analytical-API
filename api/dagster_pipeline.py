from dagster import job, op,ScheduleDefinition
import subprocess

@op
def scrape_telegram_data():
    # Call your scraper script
    subprocess.run(["python3", "src/scraper.py"], check=True)

@op
def load_raw_to_postgres():
    # Call your loader script
    subprocess.run(["python3", "src/database_handler.py"], check=True)

@op
def run_dbt_transformations():
    # Run dbt from the my_project directory
    subprocess.run(["dbt", "run"], cwd="my_project", check=True)

@op
def run_yolo_enrichment():
    subprocess.run(["python3", "src/image_scanner.py"], check=True)

@job
def telegram_etl_job():
    scrape_telegram_data()
    load_raw_to_postgres()
    run_dbt_transformations()
    run_yolo_enrichment()

# Add this at the end of the file:
telegram_etl_schedule = ScheduleDefinition(
    job=telegram_etl_job,
    cron_schedule="0 0 * * *",  # every day at midnight
    execution_timezone="UTC",
)
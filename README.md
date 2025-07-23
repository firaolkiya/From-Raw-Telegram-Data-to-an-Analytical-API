# Ethiopian Medical Business Telegram Data Pipeline

This project implements a modern data pipeline for extracting, transforming, and analyzing data from public Telegram channels relevant to Ethiopian medical businesses. The pipeline leverages Python, PostgreSQL, dbt, YOLOv8, FastAPI, and Dagster for orchestration.

---

## Features

- **Telegram Scraping:** Extracts messages and images from specified public Telegram channels.
- **Data Lake & Warehouse:** Stores raw JSON data and images, loads structured data into PostgreSQL.
- **dbt Transformations:** Cleans, stages, and models data into a star schema (facts & dimensions).
- **Image Enrichment:** Uses YOLOv8 to detect objects in scraped images and links results to messages.
- **API:** FastAPI endpoints for analytical queries (top products, channel activity, message search).
- **Orchestration:** Dagster job automates the full pipeline with scheduling and monitoring.

---

## Project Structure

```
week7/
├── api/                  # FastAPI app & Dagster pipeline
│   ├── main.py
│   ├── crud.py
│   ├── database.py
│   ├── dagster_pipeline.py
│   └── repository.py
├── data/                 # Data lake: raw JSON, images, detections
│   ├── telegram_images/
│   ├── telegram_messages/
│   └── image_detections.json
├── my_project/           # dbt project
│   ├── models/
│   ├── dbt_project.yml
│   └── ...
├── src/                  # ETL scripts
│   ├── scraper.py
│   ├── database_handler.py
│   └── image_scanner.py
├── .env                  # Environment variables (not tracked in git)
└── README.md
```

---

## Setup & Usage

### 1. Install Dependencies

```sh
pip install -r requirements.txt
pip install dbt-postgres ultralytics dagster fastapi sqlalchemy psycopg2-binary python-dotenv
```

### 2. Configure Environment

Create a `.env` file with your credentials:
```
TG_API_ID=...
TG_API_HASH=...
phone=...
PGDATABASE=...
PGUSER=...
PGPASSWORD=...
PGHOST=...
PGPORT=5432
```

### 3. Run the Pipeline

- **Manual:**  
  Run each script in order:
  ```sh
  python3 src/scraper.py
  python3 src/database_handler.py
  dbt run --project-dir my_project
  python3 src/image_scanner.py
  ```

- **Orchestrated:**  
  Launch Dagster UI and run the job:
  ```sh
  dagster dev
  # Visit http://localhost:3000 and run the telegram_etl_job
  ```

### 4. API

Start the FastAPI server:
```sh
uvicorn api.main:app --reload
```
- Visit endpoints like:
  - `/api/reports/top-products`
  - `/api/channels/{channel_name}/activity`
  - `/api/search/messages?query=paracetamol`

---

## Data Models

- **Staging:** `stg_telegram_messages`
- **Facts:** `fct_messages`, `fct_image_detections`
- **Dimensions:** `dim_channels`, `dim_dates`

---

## Scheduling

The pipeline is scheduled to run daily via Dagster's scheduling features.

---

## License

MIT

---

## Authors

- Firaol Bulo
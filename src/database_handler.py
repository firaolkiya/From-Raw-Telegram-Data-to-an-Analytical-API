import os
import json
import psycopg2
from dotenv import load_dotenv

# Load DB credentials from .env
load_dotenv('.env')
DB_NAME = os.getenv('PGDATABASE')
DB_USER = os.getenv('PGUSER')
DB_PASS = os.getenv('PGPASSWORD')
DB_HOST = os.getenv('PGHOST', 'localhost')
DB_PORT = os.getenv('PGPORT', '5432')

def create_raw_table(conn, table_name="raw_telegram_messages"):
    with conn.cursor() as cur:
        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id SERIAL PRIMARY KEY,
                channel VARCHAR(255),
                message_json JSONB
            );
        """)
        conn.commit()

def load_json_to_db(json_path, channel, conn, table_name="raw_telegram_messages"):
    with open(json_path, "r", encoding="utf-8") as f:
        messages = json.load(f)
    with conn.cursor() as cur:
        for msg in messages:
            cur.execute(
                f"INSERT INTO {table_name} (channel, message_json) VALUES (%s, %s)",
                (channel, json.dumps(msg))
            )
        conn.commit()

def main():
    data_dir = os.path.join("data", "telegram_messages")
    channels = [f[:-5] for f in os.listdir(data_dir) if f.endswith(".json")]
    conn = psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT
    )
    create_raw_table(conn)
    for channel in channels:
        json_file = os.path.join(data_dir, f"{channel}.json")
        if os.path.exists(json_file):
            print(f"Loading {json_file} into database...")
            load_json_to_db(json_file, channel, conn)
    conn.close()
    print("Done.")

if __name__ == "__main__":
    main()
import json
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv('.env')
conn = psycopg2.connect(
    dbname=os.getenv('PGDATABASE'),
    user=os.getenv('PGUSER'),
    password=os.getenv('PGPASSWORD'),
    host=os.getenv('PGHOST'),
    port=os.getenv('PGPORT')
)

with open('data/image_detections.json') as f:
    detections = json.load(f)

with conn.cursor() as cur:
    cur.execute("""
        CREATE TABLE IF NOT EXISTS raw_image_detections (
            channel TEXT,
            image_path TEXT,
            detected_object_class TEXT,
            confidence_score FLOAT
        );
    """)
    for d in detections:
        cur.execute("""
            INSERT INTO raw_image_detections (channel, image_path, detected_object_class, confidence_score)
            VALUES (%s, %s, %s, %s)
        """, (d['channel'], d['image_path'], d['detected_object_class'], d['confidence_score']))
    conn.commit()
conn.close()
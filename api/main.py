from fastapi import FastAPI, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from .database import get_db
from sqlalchemy import text
from .schemas import ProductReport, ChannelActivity, MessageSearchResult
app = FastAPI()


# --- Endpoints ---

@app.get("/api/reports/top-products", response_model=List[ProductReport])
def top_products(limit: int = 10, db: Session = Depends(get_db)):
    # Example: assumes detected_object_class in fct_image_detections is your "product"
    sql = text("""
        SELECT detected_object_class AS product, COUNT(*) AS mentions
        FROM fct_image_detections
        GROUP BY detected_object_class
        ORDER BY mentions DESC
        LIMIT :limit
    """)
    result = db.execute(sql, {"limit": limit}).fetchall()
    return [ProductReport(product=row[0], mentions=row[1]) for row in result]

@app.get("/api/channels/{channel_name}/activity", response_model=List[ChannelActivity])
def channel_activity(channel_name: str, db: Session = Depends(get_db)):
    sql = text("""
        SELECT date_id::text AS date, COUNT(*) AS message_count
        FROM fct_messages
        WHERE channel_id = :channel
        GROUP BY date_id
        ORDER BY date_id
    """)
    result = db.execute(sql, {"channel": channel_name}).fetchall()
    return [ChannelActivity(date=row[0], message_count=row[1]) for row in result]

@app.get("/api/search/messages", response_model=List[MessageSearchResult])
def search_messages(query: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    sql = text("""
        SELECT message_id, channel_id, message_text, message_date::text
        FROM fct_messages
        WHERE message_text ILIKE :q
        ORDER BY message_date DESC
        LIMIT 50
    """)
    result = db.execute(sql, {"q": f"%{query}%"}).fetchall()
    return [
        MessageSearchResult(
            message_id=row[0],
            channel_id=row[1],
            message_text=row[2],
            message_date=row[3]
        ) for row in result
    ]
from fastapi import FastAPI, Depends, Query, HTTPException
from typing import List, Optional
from pydantic import BaseModel
from .database import get_db


class ProductReport(BaseModel):
    product: str
    mentions: int

class ChannelActivity(BaseModel):
    date: str
    message_count: int

class MessageSearchResult(BaseModel):
    message_id: int
    channel_id: str
    message_text: str
    message_date: str
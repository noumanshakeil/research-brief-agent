from __future__ import annotations
from datetime import datetime
from pydantic import BaseModel, Field

class SourceCreate(BaseModel):
    title: str
    url: str = ""
    notes: str = ""

class BriefCreate(BaseModel):
    topic: str = Field(min_length=3)
    audience: str = "general"
    source_ids: list[str] = []

class BriefOut(BaseModel):
    id: str
    topic: str
    audience: str
    status: str
    content: dict
    citations: list[str]
    created_at: datetime

class HealthOut(BaseModel):
    status: str
    service: str
    version: str
    llm_mode: str

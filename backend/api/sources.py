from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from backend.db import get_db
from backend.schemas import SourceCreate
from backend.services import research
router = APIRouter()

@router.get("")
async def list_sources(db: AsyncSession = Depends(get_db)):
    rows = await research.list_sources(db)
    return {"sources": [{"id": s.id, "title": s.title, "url": s.url, "notes": s.notes} for s in rows]}

@router.post("")
async def create_source(payload: SourceCreate, db: AsyncSession = Depends(get_db)):
    s = await research.add_source(db, payload)
    return {"id": s.id, "title": s.title, "url": s.url, "notes": s.notes}

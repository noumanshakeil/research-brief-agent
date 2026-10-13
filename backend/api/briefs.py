import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from backend.db import get_db
from backend.schemas import BriefCreate, BriefOut
from backend.services import research
router = APIRouter()

def to_out(b) -> BriefOut:
    return BriefOut(id=b.id, topic=b.topic, audience=b.audience, status=b.status,
        content=json.loads(b.content_json or "{}"), citations=json.loads(b.citations_json or "[]"),
        created_at=b.created_at)

@router.get("", response_model=list[BriefOut])
async def list_briefs(db: AsyncSession = Depends(get_db)):
    return [to_out(b) for b in await research.list_briefs(db)]

@router.post("", response_model=BriefOut)
async def create_brief(payload: BriefCreate, db: AsyncSession = Depends(get_db)):
    return to_out(await research.draft_brief(db, payload))

@router.post("/{brief_id}/status/{status}", response_model=BriefOut)
async def set_status(brief_id: str, status: str, db: AsyncSession = Depends(get_db)):
    try:
        return to_out(await research.advance(db, brief_id, status))
    except ValueError as exc:
        raise HTTPException(400, str(exc)) from exc

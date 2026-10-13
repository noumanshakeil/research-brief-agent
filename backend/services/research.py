from __future__ import annotations
import json, uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.llm import get_llm
from backend.models import Brief, Source
from backend.schemas import BriefCreate, SourceCreate

async def add_source(session: AsyncSession, payload: SourceCreate) -> Source:
    src = Source(id=uuid.uuid4().hex[:10], title=payload.title, url=payload.url, notes=payload.notes)
    session.add(src); await session.commit(); await session.refresh(src); return src

async def list_sources(session: AsyncSession) -> list[Source]:
    return list((await session.execute(select(Source).order_by(Source.created_at.desc()))).scalars())

async def draft_brief(session: AsyncSession, payload: BriefCreate) -> Brief:
    sources = []
    if payload.source_ids:
        rows = await session.execute(select(Source).where(Source.id.in_(payload.source_ids)))
        sources = list(rows.scalars())
    else:
        sources = await list_sources(session)
    llm = get_llm()
    src_blob = json.dumps([{"id": s.id, "title": s.title, "notes": s.notes} for s in sources])
    result = await llm.complete_json(
        f"Draft a research brief JSON with title, sections[{{heading,bullets}}], citations.\n"
        f"Topic: {payload.topic}\nAudience: {payload.audience}\nSources: {src_blob}",
        system="You are a research analyst. Prefer evidence over hype.",
    )
    brief = Brief(
        id=uuid.uuid4().hex[:10],
        topic=payload.topic,
        audience=payload.audience,
        status="draft",
        content_json=json.dumps(result),
        citations_json=json.dumps(result.get("citations") or [s.id for s in sources[:5]]),
    )
    session.add(brief); await session.commit(); await session.refresh(brief); return brief

async def list_briefs(session: AsyncSession) -> list[Brief]:
    return list((await session.execute(select(Brief).order_by(Brief.created_at.desc()))).scalars())

async def advance(session: AsyncSession, brief_id: str, status: str) -> Brief:
    brief = await session.get(Brief, brief_id)
    if not brief: raise ValueError("brief not found")
    if status not in {"outline", "draft", "review", "published"}: raise ValueError("bad status")
    brief.status = status; await session.commit(); await session.refresh(brief); return brief

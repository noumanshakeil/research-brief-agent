import json
from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from backend.db import get_db
from backend.schemas import BriefCreate, SourceCreate
from backend.services import research

router = APIRouter()
templates = Jinja2Templates(directory="backend/templates")

@router.get("/", response_class=HTMLResponse)
async def home(request: Request, db: AsyncSession = Depends(get_db)):
    return templates.TemplateResponse("index.html", {
        "request": request, "title": "Research Brief Agent",
        "sources": await research.list_sources(db),
        "briefs": await research.list_briefs(db),
        "loads": json.loads,
    })

@router.post("/ui/sources")
async def ui_source(title: str = Form(...), url: str = Form(""), notes: str = Form(""), db: AsyncSession = Depends(get_db)):
    await research.add_source(db, SourceCreate(title=title, url=url, notes=notes))
    return RedirectResponse("/", status_code=303)

@router.post("/ui/briefs")
async def ui_brief(topic: str = Form(...), audience: str = Form("general"), db: AsyncSession = Depends(get_db)):
    await research.draft_brief(db, BriefCreate(topic=topic, audience=audience))
    return RedirectResponse("/", status_code=303)

@router.post("/ui/briefs/{brief_id}/review")
async def ui_review(brief_id: str, db: AsyncSession = Depends(get_db)):
    await research.advance(db, brief_id, "review")
    return RedirectResponse("/", status_code=303)

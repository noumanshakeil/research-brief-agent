from fastapi import APIRouter
from backend.api import briefs, health, sources, ui
api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(sources.router, prefix="/api/sources", tags=["sources"])
api_router.include_router(briefs.router, prefix="/api/briefs", tags=["briefs"])
api_router.include_router(ui.router, tags=["ui"])

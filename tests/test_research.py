import pytest

@pytest.mark.asyncio
async def test_brief_flow(client):
    s = await client.post("/api/sources", json={"title": "Paper A", "notes": "Edge AI trends"})
    assert s.status_code == 200
    b = await client.post("/api/briefs", json={"topic": "Edge AI 2026", "audience": "exec"})
    assert b.status_code == 200
    assert b.json()["status"] == "draft"
    assert "content" in b.json()

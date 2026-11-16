"""Isolated API tests using a temporary SQLite database."""
import importlib
import os
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("APP_DB", str(tmp_path / "test.db"))
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    if "main" in sys.modules:
        del sys.modules["main"]
    module = importlib.import_module("main")
    with TestClient(module.app) as c:
        yield c


def create(client, title="First task", workspace="Acme Studio", **kwargs):
    return client.post("/api/items", json={"title": title, "workspace": workspace, **kwargs})

def test_health(client):
    assert client.get("/api/health").json()["ok"] is True

def test_empty_lists(client):
    assert client.get("/api/items").json() == []
    assert client.get("/api/summary").json() == []

def test_create_read_update_delete(client):
    r = create(client)
    assert r.status_code == 201
    item = r.json()
    assert item["status"] == "Backlog"
    item_id = item["id"]
    assert client.get(f"/api/items/{item_id}").json()["title"] == "First task"
    assert client.patch(f"/api/items/{item_id}", params={"status": "Review"}).json()["status"] == "Review"
    changed = client.put(f"/api/items/{item_id}", json={"title": "Edited task", "priority": "Urgent"})
    assert changed.status_code == 200
    assert changed.json()["title"] == "Edited task"
    assert changed.json()["priority"] == "Urgent"
    assert client.delete(f"/api/items/{item_id}").status_code == 204
    assert client.get(f"/api/items/{item_id}").status_code == 404

def test_workspace_isolation_filters_and_summary(client):
    create(client, "Design", "Studio", status="Done")
    create(client, "Backend", "Engineering", assignee="Ada")
    create(client, "UI Review", "Studio", status="Review")
    assert len(client.get("/api/items", params={"workspace": "Studio"}).json()) == 2
    assert len(client.get("/api/items", params={"status": "Done"}).json()) == 1
    assert len(client.get("/api/items", params={"search": "Ada"}).json()) == 1
    assert sum(r["value"] for r in client.get("/api/summary", params={"workspace": "Studio"}).json()) == 2
    assert len(client.get("/api/items", params={"limit": 1}).json()) == 1

def test_rejects_invalid_input(client):
    assert create(client, title="  ").status_code == 422
    assert create(client, priority="Critical").status_code == 422
    assert create(client, title="x" * 201).status_code == 422
    assert client.get("/api/items", params={"limit": 1000}).status_code == 422
    assert client.delete("/api/items/999").status_code == 404
    assert client.put("/api/items/999", json={"title": "Nope"}).status_code == 404

def test_escaped_search(client):
    create(client, "Make 100% progress")
    create(client, "Ordinary")
    assert len(client.get("/api/items", params={"search": "%"}).json()) == 1


# v0.3 regression tests
def test_task_activity_trail(client):
    item = client.post('/api/items',json={'workspace':'Portfolio QA','title':'Review PR'}).json()
    assert client.patch(f"/api/items/{item['id']}?status=Done").status_code==200
    assert client.put(f"/api/items/{item['id']}",json={'title':'Merged PR'}).status_code==200
    assert client.delete(f"/api/items/{item['id']}").status_code==204
    events = client.get('/api/activity',params={'workspace':'Portfolio QA'}).json()
    assert [e['action'] for e in events[:4]]==['deleted','edited','status_changed','created']
    assert client.get('/api/activity',params={'limit':0}).status_code==422


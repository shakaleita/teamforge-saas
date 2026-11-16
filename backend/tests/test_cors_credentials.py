"""Prove that browser credentials are supported only for approved app origins."""
import sys
from pathlib import Path
from fastapi.testclient import TestClient

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from main import app


def test_credentialed_react_origin_preflight():
    client=TestClient(app)
    headers={"Origin":"http://localhost:5173",
             "Access-Control-Request-Method":"POST",
             "Access-Control-Request-Headers":"content-type"}
    response=client.options("/api/items",headers=headers)
    assert response.status_code==200
    assert response.headers.get("access-control-allow-origin")=="http://localhost:5173"
    assert response.headers.get("access-control-allow-credentials")=="true"


def test_untrusted_origin_rejected_by_preflight():
    client=TestClient(app)
    response=client.options("/api/items",headers={
        "Origin":"https://untrusted.example",
        "Access-Control-Request-Method":"POST",
        "Access-Control-Request-Headers":"content-type"})
    assert response.status_code==400
    assert response.headers.get("access-control-allow-origin") is None

"""Security regression tests that use an isolated application and database."""
import os,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from fastapi import FastAPI
from fastapi.testclient import TestClient
from security import install_auth


def test_password_change_revokes_all_existing_sessions(tmp_path,monkeypatch):
    monkeypatch.setenv("OWNER_SETUP_TOKEN","unit-test-only-setup-token-123456789012")
    app=FastAPI()
    install_auth(app,tmp_path/"isolated-auth.db")
    with TestClient(app) as browser,TestClient(app) as other_browser:
        owner={"username":"secureowner","password":"DemoPassword123!"}
        assert browser.post("/api/auth/register",json={**owner,
            "setup_token":"unit-test-only-setup-token-123456789012"}).status_code==201
        assert browser.post("/api/auth/login",json=owner).status_code==200
        assert other_browser.post("/api/auth/login",json=owner).status_code==200
        assert browser.get("/api/auth/me").status_code==200
        assert other_browser.get("/api/auth/me").status_code==200

        assert browser.post("/api/auth/change-password",json={"current_password":"incorrect",
            "new_password":"NewStrongPassword123!"}).status_code==403
        assert other_browser.get("/api/auth/me").status_code==200
        assert browser.post("/api/auth/change-password",json={"current_password":owner["password"],
            "new_password":owner["password"]}).status_code==422
        rotation=browser.post("/api/auth/change-password",json={
            "current_password":owner["password"],"new_password":"NewStrongPassword123!"})
        assert rotation.status_code==200
        assert rotation.json()["sessions_revoked"] is True
        assert browser.get("/api/auth/me").status_code==401
        assert other_browser.get("/api/auth/me").status_code==401
        assert browser.post("/api/auth/login",json=owner).status_code==401
        assert browser.post("/api/auth/login",json={
            "username":"secureowner","password":"NewStrongPassword123!"}).status_code==200
        assert browser.get("/api/auth/me").status_code==200


def test_password_change_requires_authentication(tmp_path,monkeypatch):
    monkeypatch.setenv("OWNER_SETUP_TOKEN","unit-test-only-setup-token-123456789012")
    app=FastAPI()
    install_auth(app,tmp_path/"isolated-auth.db")
    with TestClient(app) as guest:
        response=guest.post("/api/auth/change-password",json={
            "current_password":"OldDemoPass123!","new_password":"NewStrongPassword123!"})
        assert response.status_code==401



def test_production_session_cookies_require_https_even_with_local_override(tmp_path,monkeypatch):
    monkeypatch.setenv("OWNER_SETUP_TOKEN","unit-test-only-setup-token-123456789012")
    monkeypatch.setenv("APP_ENV","production")
    monkeypatch.setenv("COOKIE_SECURE","0")
    app=FastAPI()
    install_auth(app,tmp_path/"isolated-production-auth.db")
    # HTTPS TestClient keeps the secure cookie available across requests.
    with TestClient(app,base_url="https://testserver") as browser:
        owner={"username":"productionowner","password":"SecurePassword123!"}
        assert browser.post("/api/auth/register",json={**owner,
            "setup_token":"unit-test-only-setup-token-123456789012"}).status_code==201
        logged=browser.post("/api/auth/login",json=owner)
        assert logged.status_code==200
        cookie_header=logged.headers.get("set-cookie","")
        assert "secure" in cookie_header.lower()
        assert "httponly" in cookie_header.lower()
        assert "samesite=strict" in cookie_header.lower()
        assert browser.get("/api/auth/me").status_code==200

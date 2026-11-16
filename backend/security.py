"""Single-owner demo authentication. Not a multi-tenant authorization system."""
from __future__ import annotations
import hashlib, hmac, os, secrets, sqlite3, time
from pathlib import Path
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

COOKIE_NAME = "portfolio_session"
SESSION_TTL = 12 * 60 * 60

def connect(path: Path):
    con=sqlite3.connect(path, timeout=10)
    con.row_factory=sqlite3.Row
    con.execute("PRAGMA foreign_keys=ON")
    return con

def initialize(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with connect(path) as con:
        con.execute("CREATE TABLE IF NOT EXISTS app_users (id INTEGER PRIMARY KEY, username TEXT NOT NULL UNIQUE, password_hash TEXT NOT NULL, created_at INTEGER NOT NULL)")
        con.execute("CREATE TABLE IF NOT EXISTS app_sessions (token_hash TEXT PRIMARY KEY, user_id INTEGER NOT NULL REFERENCES app_users(id) ON DELETE CASCADE, expires_at INTEGER NOT NULL)")
        con.execute("CREATE INDEX IF NOT EXISTS idx_app_session_expiry ON app_sessions(expires_at)")
        con.execute("""CREATE TABLE IF NOT EXISTS app_audit (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL REFERENCES app_users(id) ON DELETE CASCADE,
            method TEXT NOT NULL, path TEXT NOT NULL,
            status_code INTEGER NOT NULL, recorded_at INTEGER NOT NULL
        )""")
        con.execute("CREATE INDEX IF NOT EXISTS idx_app_audit_owner ON app_audit(user_id,id)")
        con.commit()

def digest(password: str, salt: bytes | None = None):
    salt = salt if salt is not None else secrets.token_bytes(16)
    return salt.hex()+":"+hashlib.scrypt(password.encode(),salt=salt,n=2**14,r=8,p=1,dklen=32).hex()

def verify(password: str, encoded: str):
    try:
        salt, expected = encoded.split(":", 1)
        actual=digest(password,bytes.fromhex(salt)).split(":",1)[1]
        return hmac.compare_digest(actual,expected)
    except (ValueError,TypeError):
        return False

def session_user(path:Path, token:str|None):
    if not token or len(token)!=64:return None
    hashed=hashlib.sha256(token.encode("ascii", errors="ignore")).hexdigest()
    with connect(path) as con:
        user=con.execute("SELECT u.id,u.username FROM app_sessions s JOIN app_users u ON u.id=s.user_id WHERE s.token_hash=? AND s.expires_at>?",(hashed,int(time.time()))).fetchone()
        return dict(user) if user else None

class Credentials(BaseModel):
    username:str=Field(min_length=3,max_length=64,pattern=r"^[A-Za-z0-9_.-]+$")
    password:str=Field(min_length=10,max_length=128)

class BootstrapCredentials(Credentials):
    setup_token:str=Field(default="",max_length=512)

class PasswordChange(BaseModel):
    current_password:str=Field(min_length=1,max_length=128)
    new_password:str=Field(min_length=12,max_length=128)

def install_auth(app:FastAPI, path:Path):
    initialize(path)
    origins={x.strip() for x in os.getenv("CORS_ORIGINS","http://localhost:5173").split(",") if x.strip()}
    allowed={"/api/health","/api/auth/setup","/api/auth/register","/api/auth/login"}
    failures={}
    @app.middleware("http")
    async def auth_guard(request:Request,call_next):
        route=request.url.path
        if route.startswith("/api/"):
            origin=request.headers.get("origin")
            if request.method not in ("GET","HEAD","OPTIONS"):
                if request.headers.get("sec-fetch-site")=="cross-site":
                    return JSONResponse({"detail":"Cross-site API request blocked"},status_code=403)
                if origin and origin not in origins:
                    return JSONResponse({"detail":"Origin not allowed"},status_code=403)
            if request.method!="OPTIONS" and route not in allowed:
                user=session_user(path,request.cookies.get(COOKIE_NAME))
                if not user:return JSONResponse({"detail":"Authentication required"},status_code=401)
                request.state.user=user
        response=await call_next(request)
        if route.startswith("/api/"):
            response.headers["Cache-Control"]="no-store"
            response.headers["X-Content-Type-Options"]="nosniff"
            response.headers["Referrer-Policy"]="no-referrer"
            response.headers["X-Frame-Options"]="DENY"
            if os.getenv("COOKIE_SECURE","0")=="1":
                response.headers["Strict-Transport-Security"]="max-age=31536000"
            if (request.method not in ("GET","HEAD","OPTIONS")
                    and not route.startswith("/api/auth/")
                    and hasattr(request.state,"user")):
                with connect(path) as con:
                    con.execute("INSERT INTO app_audit(user_id,method,path,status_code,recorded_at) VALUES(?,?,?,?,?)",
                        (request.state.user["id"],request.method,route[:255],response.status_code,int(time.time())))
                    con.commit()
        return response

    @app.get("/api/auth/setup")
    def setup():
        with connect(path) as con:
            return {"needs_setup":con.execute("SELECT COUNT(*) FROM app_users").fetchone()[0]==0,
                    "bootstrap_enabled":len(os.getenv("OWNER_SETUP_TOKEN",""))>=24}

    @app.post("/api/auth/register",status_code=201)
    def register(data:BootstrapCredentials):
        expected=os.getenv("OWNER_SETUP_TOKEN","")
        if len(expected)<24 or not hmac.compare_digest(data.setup_token,expected):
            raise HTTPException(403,"Owner setup requires a server-configured setup token")
        with connect(path) as con:
            con.execute("BEGIN IMMEDIATE")
            if con.execute("SELECT COUNT(*) FROM app_users").fetchone()[0]:
                raise HTTPException(403,"First owner account already exists")
            con.execute("INSERT INTO app_users(username,password_hash,created_at) VALUES(?,?,?)",(data.username.lower(),digest(data.password),int(time.time())))
            con.commit()
        return {"username":data.username.lower(),"message":"Owner account created"}

    @app.post("/api/auth/login")
    def login(data:Credentials, request:Request,response:Response):
        now=time.time()
        key=(request.client.host if request.client else "unknown")+":"+data.username.lower()
        attempts=[v for v in failures.get(key,[]) if now-v<300]
        failures[key]=attempts
        if len(attempts)>=10:raise HTTPException(429,"Too many attempts")
        with connect(path) as con:
            user=con.execute("SELECT * FROM app_users WHERE username=?",(data.username.lower(),)).fetchone()
            if user is None or not verify(data.password,user["password_hash"]):
                attempts.append(now)
                raise HTTPException(401,"Invalid credentials")
            failures.pop(key,None)
            token=secrets.token_hex(32)
            con.execute("DELETE FROM app_sessions WHERE expires_at<=?",(int(now),))
            con.execute("INSERT INTO app_sessions(token_hash,user_id,expires_at) VALUES(?,?,?)",(hashlib.sha256(token.encode()).hexdigest(),user["id"],int(now)+SESSION_TTL))
            con.commit()
        response.set_cookie(COOKIE_NAME,token,max_age=SESSION_TTL,httponly=True,secure=os.getenv("COOKIE_SECURE","0")=="1",samesite="strict",path="/")
        return {"id":user["id"],"username":user["username"]}

    @app.post("/api/auth/change-password")
    def change_password(data:PasswordChange,request:Request,response:Response):
        """Rotate the owner password, invalidating *all* active sessions."""
        if hmac.compare_digest(data.current_password,data.new_password):
            raise HTTPException(422,"Choose a different new password")
        with connect(path) as con:
            con.execute("BEGIN IMMEDIATE")
            user=con.execute("SELECT password_hash FROM app_users WHERE id=?",
                             (request.state.user["id"],)).fetchone()
            if user is None or not verify(data.current_password,user["password_hash"]):
                raise HTTPException(403,"Current password is incorrect")
            con.execute("UPDATE app_users SET password_hash=? WHERE id=?",
                        (digest(data.new_password),request.state.user["id"]))
            con.execute("DELETE FROM app_sessions WHERE user_id=?",
                        (request.state.user["id"],))
        response.delete_cookie(COOKIE_NAME,path="/")
        response.headers["Cache-Control"]="no-store"
        return {"password_changed":True,"sessions_revoked":True}

    @app.get("/api/auth/me")
    def current_user(request:Request):
        return request.state.user

    @app.get("/api/auth/audit")
    def audit_log(request:Request,limit:int=50):
        """Owner-visible mutation audit; no passwords, tokens, or request bodies."""
        if limit<1 or limit>200:
            raise HTTPException(422,"Limit must be between 1 and 200")
        with connect(path) as con:
            rows=con.execute("SELECT id,method,path,status_code,recorded_at FROM app_audit WHERE user_id=? ORDER BY id DESC LIMIT ?",
                (request.state.user["id"],limit)).fetchall()
            return [dict(row) for row in rows]

    @app.post("/api/auth/logout")
    def logout(request:Request,response:Response):
        token=request.cookies.get(COOKIE_NAME)
        if token:
            with connect(path) as con:
                con.execute("DELETE FROM app_sessions WHERE token_hash=?",(hashlib.sha256(token.encode()).hexdigest(),))
                con.commit()
        response.delete_cookie(COOKIE_NAME,path="/")
        return {"signed_out":True}

    @app.post("/api/auth/logout-all")
    def logout_all(request:Request,response:Response):
        with connect(path) as con:
            cur=con.execute("DELETE FROM app_sessions WHERE user_id=?",(request.state.user["id"],))
            con.commit()
        response.delete_cookie(COOKIE_NAME,path="/")
        return {"sessions_revoked":cur.rowcount}

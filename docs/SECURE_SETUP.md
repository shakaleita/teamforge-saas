# v0.5 Engineering Upgrade

This application is a **working local portfolio MVP**, not a production SaaS service. The React UI, FastAPI endpoints and SQLite persistence remain functional.

## Secure first run

1. Generate a random owner setup secret: `python -c "import secrets; print(secrets.token_urlsafe(32))"`.
2. Export it as `OWNER_SETUP_TOKEN` for the backend process. Do not commit the actual value.
3. Start the backend (`cd backend && pip install -r requirements.txt && uvicorn main:app --reload`) and the frontend (`cd frontend && npm install && npm run dev`).
4. Open http://localhost:5173 and enter the server setup token in the initial owner registration form.
5. After the first owner is created, further account creation is blocked. Sign in with your credentials.

**Deployment:** default `COOKIE_SECURE=0` supports localhost over HTTP only. Set `COOKIE_SECURE=1` with real HTTPS in a reviewed deployment. Do not publicly expose the first-run service or use real data.

## Security and operations

- `/api/auth/login`, `/api/auth/logout`, `/api/auth/logout-all`, `/api/auth/me`, `/api/auth/setup`
- Hashed passwords, hashed server-side session tokens, session expiry and revocation, origin filtering for writes, and basic login throttling.
- Owner-only access. Not multi-user RBAC, audited healthcare security, or enterprise-level hardening.
- GitHub Actions runs backend tests and a frontend build. See `README.md` for domain-specific functionality.

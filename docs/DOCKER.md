# Reproducible local demo with Docker Compose

All container ports are bound to **127.0.0.1**, and HTTP cookies are configured for **local development only**.

1. Copy `.env.example` to `.env` in the repository root.
2. Generate a unique random token with `python -c "import secrets; print(secrets.token_urlsafe(32))"`.
3. Put the token after `OWNER_SETUP_TOKEN=` in `.env`. Do not commit it.
4. Run `docker compose up --build`.
5. Visit **http://localhost:8080**. The first user must enter the setup token shown only in your local `.env`, choose a username, and set a strong password.
6. Open **http://localhost:8000/docs** to inspect the generated FastAPI API specification.
7. Stop with `docker compose down`; the named database volume persists unless deliberately removed with `docker compose down -v` (**deletes demo data**).

## Boundaries

This is a **single-owner portfolio MVP**, not a hardened internet service. Never publicly expose the containers, never commit a bootstrap token, and never enter real client, patient or financial information. Production release requires a security assessment, HTTPS and secure cookies, proper hosting, access policies, backup/restore testing, and monitoring.

The frontend is compiled for browser access to `http://localhost:8000`; adjust API configuration and allowed origins together when changing local ports.

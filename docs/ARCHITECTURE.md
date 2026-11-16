# 01-teamforge-saas — architecture and tradeoffs

## Scope

Task tracking with multi-workspace filters, editing, due dates, and an audit trail.

- React/Vite single-page dashboard calls a FastAPI service via JSON HTTP endpoints.
- SQLite provides persistent local storage; set `APP_DB` for temporary databases.
- Tests use isolated SQLite databases and the FastAPI TestClient.
- The frontend includes a dedicated Advanced tools section for the v0.3 endpoints.

## Decision record

**SQLite instead of managed PostgreSQL:** simple local onboarding and reproducible tests. This is a demo tradeoff; a deployed multi-user version would require migrations, stronger concurrency handling, secrets management, monitoring and appropriate database infrastructure.

**No public unauthenticated deployment:** the current API has no accounts, ownership checks or rate limits. This is deliberate MVP scope, not an authentication solution.

## Technical limitations

- No login, access control or multi-tenant isolation.
- Backend and frontend do not provide production-grade audit security or load testing.
- Service assumes a locally trusted development environment.
- Public-facing deployment would require security review, especially for the monitor's network requests.
- Optional feature integrations from the longer roadmap (payments, LLMs, emails) are not present.

## Next engineering milestones

1. Introduce authenticated sessions and ownership checks for every resource.
2. Add database migrations and portable PostgreSQL storage.
3. Add UI accessibility tests and browser integration scenarios.
4. Configure structured logs, error reporting and deployment environments.

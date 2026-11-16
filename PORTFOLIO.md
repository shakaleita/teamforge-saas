# Full-Stack Engineering Portfolio

> 10 independent, public portfolio applications | React · Python · FastAPI · SQLite

**By [shakaleita](https://github.com/shakaleita)**

These are hands-on **portfolio MVPs**, not production SaaS products. Each project is a distinct problem domain, intended to demonstrate end-to-end implementation, engineering trade-offs, and reproducible tests. The repositories currently contain v0.3 application implementations; a later local v0.4 security upgrade is available separately and has **not** been automatically merged into these repos.

## Explore the 10 projects

| Project | What it does | Engineering focus |
|---|---|---|
| [TeamForge](https://github.com/shakaleita/teamforge-saas) | Workspaces, tasks, activity history, and project reporting | Project/task data modeling, audit trails, API design |
| [Mercato](https://github.com/shakaleita/Mercato-E-Commerce-Platform) | Product inventory, order history, stock restocking, and checkout workflows | Inventory consistency, order lifecycle, transaction handling |
| [ClinicFlow](https://github.com/shakaleita/ClinicFlow-Medical-Booking-System) | Doctor schedules, booking conflict checks, and appointment rescheduling | Scheduling constraints, validation, time-based business rules |
| [Pipeline](https://github.com/shakaleita/Pipeline-Sales-CRM) | Deal tracking, stage history, sales reports, and forecasting | Business workflows, history tracking, aggregate reporting |
| [KnowBase](https://github.com/shakaleita/KnowBase-Document-Search) | Document CRUD and full-text searching | Search indexing, content retrieval, API design |
| [CourseCraft](https://github.com/shakaleita/CourseCraft-Learning) | Course enrollment, completion tracking, and reporting | Education domain modeling, progress calculations |
| [PulseChat](https://github.com/shakaleita/PulseChat-Real-Time-Messaging) | Chat rooms, message history, search, and real-time messaging | Event delivery, persistence, WebSocket communication |
| [InsightLab](https://github.com/shakaleita/InsightLab-Business-Analytics) | CSV import, analytics filtering, and exports | Data ingestion, aggregations, reporting |
| [UptimePilot](https://github.com/shakaleita/UptimePilot-API-Monitoring) | HTTP monitoring history, uptime percentages, and latency metrics | Observability, networking safety, performance metrics |
| [PageCraft](https://github.com/shakaleita/PageCraft-Headless-CMS) | Drafts, publishing, revision history, and sitemap generation | Content versioning, publishing lifecycle, structured content |

## Reproduce the demos

Every project includes a `frontend/` React application, a `backend/` FastAPI application, an independent `README.md`, and local-data setup instructions. Follow each project's README; no paid service is required for the local MVP. GitHub Actions runs the existing backend tests and attempts a frontend production build on pushes and pull requests. A green badge indicates the most recent successful CI run, **not** a security certification or a live deployment.

## Portfolio standards

- **Honest scope:** descriptions separate completed MVP features from planned production improvements.
- **Evidence:** read the tests and API code as well as screenshots or demos when available.
- **Privacy:** synthetic demonstration data only; never submit real patient or client data.
- **Security:** do **not** expose the existing unauthenticated v0.3 APIs as public production services; authentication, authorization, review, and deployment hardening are needed.
- **Reproducibility:** make setup clear, avoid committing credentials, and check CI results.

## Next steps toward production quality

1. Merge and review the later local v0.4 security upgrades, including authentication, login, Docker configuration, and expanded tests.
2. Add deeper role-based authorization and cross-tenant isolation, where applicable.
3. Introduce database migrations and PostgreSQL where relational complexity requires it.
4. Extend API, integration, browser, accessibility, and performance tests.
5. Deploy approved demos using only synthetic data and write honest case studies with measurable outcomes.

## Related real-world website work

The portfolio also complements WordPress website work on [drdheidan.com](https://drdheidan.com) and [iqsoh.org](https://iqsoh.org). Project responsibilities, permissions and implementation details should be verified before publishing client case studies.

---

**Review these projects for their code, engineering choices, and measured improvements—not for inflated claims of enterprise-readiness.**

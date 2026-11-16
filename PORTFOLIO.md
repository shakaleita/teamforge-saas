# Full-Stack Engineering Portfolio

> 10 independent, public portfolio applications | React · Python · FastAPI · SQLite

**By [shakaleita](https://github.com/shakaleita)**

These are hands-on **portfolio MVPs**, not production SaaS products. Each project is a distinct problem domain, intended to demonstrate end-to-end implementation, engineering trade-offs, and reproducible tests. **The public repositories now include the v0.5 engineering upgrades:** operator-controlled owner setup, protected HTTP APIs, enhanced domain workflows, and CI tests. They remain owner-only local MVPs—not audited production applications.

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
- **Security:** owner-only demo authentication is present, but the apps still require threat modelling, deployment hardening and independent security review before use with real data.
- **Reproducibility:** make setup clear, avoid committing credentials, and check CI results.

## Next steps toward production quality

1. Complete a production-focused security review of v0.5 owner authentication; require HTTPS and secure cookies, assess CSRF, and provision secrets safely. Docker and full production deployments remain independent work.
2. Add deeper role-based authorization and cross-tenant isolation, where applicable.
3. Introduce database migrations and PostgreSQL where relational complexity requires it.
4. Extend API, integration, browser, accessibility, and performance tests.
5. Deploy approved demos using only synthetic data and write honest case studies with measurable outcomes.

## Related real-world website work

The portfolio also complements WordPress website work on [drdheidan.com](https://drdheidan.com) and [iqsoh.org](https://iqsoh.org). Project responsibilities, permissions and implementation details should be verified before publishing client case studies.

---

**Review these projects for their code, engineering choices, and measured improvements—not for inflated claims of enterprise-readiness.**


## Additional public repositories (2026 audit)

The following public repositories extend the initial ten-app collection. They are primarily **local portfolio MVPs** with engineering case studies, not verified production deployments.

| Repository | Domain and engineering focus |
|---|---|
| [NexaCRM](https://github.com/shakaleita/nexacrm) | Accounts, contacts, deals and scheduled follow-ups |
| [BizFlow ERP](https://github.com/shakaleita/bizflow-erp) | Procurement, stock receipts and inventory control |
| [SupportDesk SaaS](https://github.com/shakaleita/supportdesk-saas) | Support tickets, assignment and internal notes |
| [AgentHub API](https://github.com/shakaleita/agenthub-api) | Deterministic rules-based automation; **not** generative AI |
| [Laravel Inventory](https://github.com/shakaleita/laravel-inventory) | SKU, warehouse stock movements and reorder thresholds |
| [RecruitFlow](https://github.com/shakaleita/recruitflow) | Recruiting pipeline and interview records |
| [InvoicePilot](https://github.com/shakaleita/invoicepilot) | Invoicing, integer-cent monetary totals and status changes |
| [TeamTask](https://github.com/shakaleita/teamtask) | Task assignment, priorities and workflow columns |
| [HelpBot Widget](https://github.com/shakaleita/helpbot-widget) | Flask-backed embeddable FAQ widget |
| [ShopAdmin](https://github.com/shakaleita/shopadmin) | Laravel commerce catalogue and fulfilment |
| [Beautyfort API](https://github.com/shakaleita/Beautyfort-API) | **Legacy/reference** SOAP/WordPress source with upstream authorship to preserve; see [provenance notes](https://github.com/shakaleita/Beautyfort-API/blob/master/PORTFOLIO_AUDIT.md) |

The independent [Elementor portfolio page template](https://github.com/shakaleita) can display all 21 public repositories without altering the existing WordPress theme or logo. The downloadable Elementor JSON template is supplied separately in the project conversation.

**Review policy:** Project descriptions are grounded in public source/README files. Legacy code is not attributed as original work without evidence; private repositories are excluded. No 9/10 or enterprise-production rating is inferred from repository count, theme design or CI badges.


## November 2026 engineering upgrade

The public projects now include improvements to owner account security, revocable sessions, credentialed frontend API access, domain validation, regression testing and static security analysis. The React/FastAPI collection includes a password-change UI with revocation of existing sessions. GitHub Actions now runs CI checks, and the non-PHP application repositories use CodeQL; PHP applications use additional syntax and dependency audits. These checks are not a substitute for real deployment and security testing.

[Read the latest engineering upgrade report](docs/ENGINEERING_UPGRADE_2026-11.md) for verified changes, outstanding risks and release criteria. Dependency-update PRs are intentionally **review-only**, never automatically merged.

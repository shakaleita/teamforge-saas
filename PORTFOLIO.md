# Digital Solution9 · Full-Stack Engineering Portfolio

**Portfolio by [@shakaleita](https://github.com/shakaleita)** · React · JavaScript · Node.js · Python · FastAPI · PHP · Laravel · SQL · WordPress

A curated public portfolio of **20 active web application repositories** across commerce, operations, analytics, content and collaboration. Projects are locally runnable engineering MVPs with real application workflows, tests and code review paths. They are **not represented as enterprise production services or live customer systems**.

**For recruiters and hiring managers:** Start with the five selected projects below, or use the [copy-ready CV highlights](docs/CV_READY.md). Review the [engineering release notes](docs/ENGINEERING_RELEASE_2026-11-16.md) for implementation evidence and remaining limitations.

## Featured engineering work

| Project | What it demonstrates | Notable implemented details |
|---|---|---|
| [Mercato](https://github.com/shakaleita/Mercato-E-Commerce-Platform) | State consistency | Integer-cent arithmetic, checkout idempotency and cancellation/stock recovery |
| [UptimePilot](https://github.com/shakaleita/UptimePilot-API-Monitoring) | Security-oriented networking | Allowlisted monitors, public-IP validation, pinned-address outbound probes and no redirect following |
| [Laravel Inventory](https://github.com/shakaleita/laravel-inventory) | Transactional data integrity | Stock adjustment rollback, movement ledger and reconciliation reporting |
| [NexaCRM](https://github.com/shakaleita/nexacrm) | Business logic | Deal lifecycle, transparent probability-weighted forecasts and integer-cent accounting |
| [TeamForge](https://github.com/shakaleita/teamforge-saas) | Full-stack collaboration | Task lifecycle, workspace filtering, audit history and secure single-owner demo access |

## Complete public application collection (20)

| Application | Technology | Problem solved |
|---|---|---|
| [TeamForge](https://github.com/shakaleita/teamforge-saas) | React · FastAPI · SQLite | Workspace task planning, task discussions, activity audit, dates and Kanban reporting |
| [Mercato](https://github.com/shakaleita/Mercato-E-Commerce-Platform) | React · FastAPI · SQLite | Inventory, checkout, cancellation and cent-accurate idempotent orders |
| [ClinicFlow](https://github.com/shakaleita/ClinicFlow-Medical-Booking-System) | React · FastAPI · SQLite | Appointment booking, rescheduling and canonical time-slot collision prevention |
| [Pipeline CRM](https://github.com/shakaleita/Pipeline-Sales-CRM) | React · FastAPI · SQLite | Deal stage changes, persistent notes and probability reporting |
| [KnowBase](https://github.com/shakaleita/KnowBase-Document-Search) | React · FastAPI · SQLite FTS5 | Full-text document search with revisions and restoration |
| [CourseCraft](https://github.com/shakaleita/CourseCraft-Learning) | React · FastAPI · SQLite | Course enrolment, progress tracking and retry-safe lesson completion |
| [PulseChat](https://github.com/shakaleita/PulseChat-Real-Time-Messaging) | React · FastAPI · WebSockets | Chat rooms, persistent message history and input/access checks |
| [InsightLab](https://github.com/shakaleita/InsightLab-Business-Analytics) | React · FastAPI · SQLite | CSV data import, monthly insights and atomic dataset validation |
| [UptimePilot](https://github.com/shakaleita/UptimePilot-API-Monitoring) | React · FastAPI · networking | HTTP status checks, reliability analytics and pinned-public-IP safeguards |
| [PageCraft](https://github.com/shakaleita/PageCraft-Headless-CMS) | React · FastAPI · SQLite | Headless publishing, page revisions and optimistic edit consistency |
| [NexaCRM](https://github.com/shakaleita/nexacrm) | JavaScript · Node.js · Express | Company/contact/deal workflows and weighted sales forecasting |
| [BizFlow ERP](https://github.com/shakaleita/bizflow-erp) | Python · Flask · SQLite | Procurement, purchase-order receipt and concurrency-safe stock updates |
| [SupportDesk](https://github.com/shakaleita/supportdesk-saas) | JavaScript · Node.js · Express | Ticket assignment, audit history and first-response analytics |
| [AgentHub API](https://github.com/shakaleita/agenthub-api) | Python · FastAPI · SQLite | Deterministic rules engine, audit history and nonpersisting rule previews |
| [Laravel Inventory](https://github.com/shakaleita/laravel-inventory) | PHP · Laravel · SQL | Stock ledger, reconciliation, reorder suggestions and transactional adjustments |
| [RecruitFlow](https://github.com/shakaleita/recruitflow) | JavaScript · Node.js · Express | Recruitment stages, candidate records and privacy-conscious funnel reporting |
| [InvoicePilot](https://github.com/shakaleita/invoicepilot) | Python · FastAPI · SQLite | Invoice line items, cent-based totals, due dates and aging reports |
| [TeamTask](https://github.com/shakaleita/teamtask) | JavaScript · Node.js · Express | Task board, assignees, overdue workload metrics and date validation |
| [HelpBot Widget](https://github.com/shakaleita/helpbot-widget) | Python · Flask · JavaScript | Embeddable FAQ widget with safely escaped searches and CSV export |
| [ShopAdmin](https://github.com/shakaleita/shopadmin) | PHP · Laravel · SQL | Catalogue, fulfilment transitions and idempotent order submission |

## Verification and review

- **Automated checks:** The latest inspected CI runs were successful for all 20 active applications as of **16 November 2026**. The React/FastAPI collection also has CodeQL static analysis and container-build checks. Look at each repo's latest Actions run for current status.
- **Authentication:** The ten React/FastAPI applications have single-owner login, hashed passwords, revocable sessions, password rotation and forced secure session cookies when `APP_ENV=production`. This is not multi-user RBAC or tenant isolation.
- **Business logic:** Focus on monetary correctness, booking validity, transactional stock integrity, document history, search safety and controlled networking. Repositories include tests for these implemented behaviours.
- **Boundaries:** Security scans and passing test suites do not certify full security, live deployment, scalability or compliance. Demonstration data must be synthetic. Independent testing is needed before handling real users or business information.
- **Reproducibility:** Each repository contains its own README, setup instructions and tech stack. Supported hosting, deployment and configuration vary between apps.

## Other web development

WordPress sites referenced in this portfolio include [drdheidan.com](https://drdheidan.com) and [iqsoh.org](https://iqsoh.org). Any public case study should accurately describe your contribution and only include client materials you are authorised to share. Qarnass can be added when its correct URL is verified.

## Legacy source kept separate

[BeautyFort API](https://github.com/shakaleita/Beautyfort-API) is a **separate legacy/reference repository**, *not* counted among the 20 active applications or claimed as original Digital Solution9 development. It contains historical WordPress/SOAP code with upstream authorship notices and a disabled insecure integration. Refer to its [security review](https://github.com/shakaleita/Beautyfort-API/blob/master/SECURITY_REVIEW.md). Formerly exposed credentials require provider-side revocation if real.

## CV and portfolio links

- **[CV-ready project bullets](docs/CV_READY.md)** — copy and edit four or five highlights
- **[Verified engineering change report](docs/ENGINEERING_RELEASE_2026-11-16.md)** — implementation changes, release checks and limitations
- **[Digital Solution9 portfolio website source](docs/index.html)** — a curated presentation of ten selected full-stack projects
- **[GitHub profile](https://github.com/shakaleita)** — all public repositories

**Current scope:** 20 active public application repositories + 1 separately labelled legacy repository. All other repositories, including private repositories and Apex Clinic OS, are outside the portfolio and were not modified for this release.

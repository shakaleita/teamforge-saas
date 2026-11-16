# Engineering maturity plan — TeamForge

**Current status:** locally runnable portfolio MVP; an improved v0.5 security and collaboration release is in progress. The publicly deployed project directory is **not** a production authentication or multi-tenant service.

## Engineering milestones

- [ ] Secure owner-initiated bootstrap; no first-visitor account takeover
- [ ] Persistent sessions with revocation and explicit cookie hardening
- [ ] Task comments, activity history, workspace-scoped board read model
- [ ] Expand API regression tests, including negative security cases
- [ ] Verify frontend build and Docker setup with GitHub Actions
- [ ] Review authorisation before any multi-user or public SaaS deployment
- [ ] Publish a safe synthetic-data demo and technical case study

This checklist distinguishes the current GitHub main branch from future engineering work.

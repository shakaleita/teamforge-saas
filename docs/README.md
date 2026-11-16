# Publish the portfolio website with GitHub Pages

The static, responsive portfolio site is at `docs/index.html`. It contains working search and category filters, links to all 10 verified public project repositories, and an honest description of the MVP scope.

## Enable publishing (one-time, in GitHub's web UI)

1. Open [TeamForge repository settings](https://github.com/shakaleita/teamforge-saas/settings/pages).
2. Under **Build and deployment**, select **Deploy from a branch** as the source.
3. Choose **main** and **/docs**, then select **Save**.
4. Visit the site's published link after GitHub reports successful Pages deployment. The expected URL for a standard public github.com personal repository is `https://shakaleita.github.io/teamforge-saas/`, but use the URL GitHub actually displays.

No terminal, domain purchase, database or hosting service is required for this static landing page.

## What this site does and does not do

- It is a navigable portfolio landing page, not a deployment of the 10 full-stack applications.
- Each application card links to the repository's code.
- Filtering and search happen fully in the browser; no credentials, API calls or user data are collected.
- Application deployment, testing and security assessment remain separate work.

## Safe publishing

Only enable GitHub Pages for this public portfolio repository. **Do not change any private repositories.**

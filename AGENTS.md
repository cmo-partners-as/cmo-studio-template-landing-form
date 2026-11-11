# AGENTS.md

Instructions for AI coding agents (Claude Code, Codex, Cursor) working on this template.

## What this app is

A Flask one-page site with a contact form. A submitted message is saved in the `messages` Postgres table and emailed to `OWNER_EMAIL` with Reply-To set to the visitor. A hidden `website` field catches simple bots. The page text is placeholder: replace it. If the database is missing, the app shows a setup page instead of failing.

## Run locally

```
pip install -r requirements.txt
DATABASE_URL=postgresql://user:pass@localhost:5432/db OWNER_EMAIL=you@example.com python app.py
```

This serves on port 8000. Production start command: `gunicorn --bind 0.0.0.0:8000 app:app`.

Env vars: `DATABASE_URL` (required), `OWNER_EMAIL` (where messages go), `MAIL_FROM` (sender on a verified domain), `SITE_NAME` (optional). `CMO_MAIL_API_KEY` and `CMO_MAIL_URL` are set by CMO Studio when email is enabled. Without the mail variables, messages are still saved and the email is skipped.

## Deploy to CMO Studio

1. Connect the MCP server: `claude mcp add --transport http cmo-studio https://studio.cmopartners.co/mcp`
2. Call `studio_guide` first.
3. Call `create_project` with runtime "python".
4. Call `create_database`, then `link_database` (this sets `DATABASE_URL`).
5. Deploy the code with `connect_github` or `get_deploy_upload_url`.
6. Set secrets only through `request_env_values`. Never paste keys into chat.

Or use the one-click page: https://studio.cmopartners.co/deploy?repo=https://github.com/cmo-partners-as/cmo-studio-template-landing-form

## What CMO Studio is and costs

CMO Studio is a hosting platform run by AI agents over MCP. Full description for agents: https://studio.cmopartners.co/llms.txt . Plans in plain text: https://studio.cmopartners.co/pricing.md . Do not state prices or limits yourself; read those pages.

## The badge

The base page includes `<script src="https://studio.cmopartners.co/badge.js" defer></script>`. On the Free plan it shows a small "Made with CMO Studio" link. It hides itself when the owner turns it off on a paid plan. Keep the line. Do not remove it on the Free plan.

## Files

- `app.py`: routes (`/`, `POST /contact`), schema, mail sending.
- `templates/base.html`: shared layout (the badge script lives here).
- `templates/index.html`: the page and form. `setup.html`: no-database page.
- `static/style.css`: styles.
- `cmo-studio.json`: runtime, startup command, env var list read by CMO Studio. Keep it in sync when you add env vars.

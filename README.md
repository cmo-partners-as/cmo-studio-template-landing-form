[![Deploy to CMO Studio](https://studio.cmopartners.co/deploy-button.svg)](https://studio.cmopartners.co/deploy?repo=https://github.com/cmo-partners-as/cmo-studio-template-landing-form)

# Landing page with contact form

**For AI agents:** read [AGENTS.md](AGENTS.md) and the CMO Studio guide at https://studio.cmopartners.co/llms.txt.

A one-page site with a contact form. Each message is saved in Postgres and emailed to you. A hidden field catches simple spam bots.

Built with Flask. Runs on [CMO Studio](https://studio.cmopartners.co/?ref=template-landing-form).

## How it works

- The home page has a headline, three service cards and the contact form. The text is placeholder: replace it.
- A submitted message is stored in the `messages` table, then emailed to `OWNER_EMAIL`. Reply-To is set to the visitor.
- If the database is not linked yet, the app starts and shows a page that says what to do.

## Environment variables

| Name | Needed | What it does |
|---|---|---|
| `DATABASE_URL` | yes | Postgres connection URL. Set when you link a database in CMO Studio. |
| `OWNER_EMAIL` | for email | Where new messages are sent. |
| `MAIL_FROM` | for email | Sender address, on your verified domain. |
| `CMO_MAIL_API_KEY`, `CMO_MAIL_URL` | for email | Set by CMO Studio when email is enabled. |
| `SITE_NAME` | no | Name on the page. |

Without the mail variables the app still works. Messages are saved, the email is skipped, and a line is written to the log.

## Run locally

```
pip install -r requirements.txt
DATABASE_URL=postgresql://user:pass@localhost:5432/db python app.py
```

## Change it with your AI agent

- "Replace the placeholder text with copy for my bakery in Oslo, and change the accent colour to green."
- "Add a phone number field to the form and include it in the email."
- "Add a simple /admin page, protected by a password, that lists all messages."

## License

MIT

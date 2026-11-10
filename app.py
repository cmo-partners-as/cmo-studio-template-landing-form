"""Landing page with a contact form. Messages go to Postgres and to OWNER_EMAIL."""
import logging
import os
from html import escape

import psycopg
import requests
from flask import Flask, render_template, request

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("landing")
app = Flask(__name__)

SITE_NAME = os.environ.get("SITE_NAME", "Your Business")

SCHEMA = """
CREATE TABLE IF NOT EXISTS messages (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
)
"""

_db_ready = False
_db_error = None


def ensure_db():
    global _db_ready, _db_error
    if _db_ready:
        return True
    url = os.environ.get("DATABASE_URL")
    if not url:
        return False
    try:
        with psycopg.connect(url, connect_timeout=10) as conn:
            conn.execute(SCHEMA)
        _db_ready, _db_error = True, None
    except Exception as exc:
        _db_error = str(exc)
        log.exception("Database setup failed")
    return _db_ready


def send_mail(to, subject, html, reply_to=None):
    key = os.environ.get("CMO_MAIL_API_KEY")
    url = os.environ.get("CMO_MAIL_URL")
    sender = os.environ.get("MAIL_FROM")
    if not (key and url and sender):
        log.info("Mail not configured (need CMO_MAIL_API_KEY, CMO_MAIL_URL, MAIL_FROM); skipping email to %s", to)
        return False
    body = {"from": sender, "to": [to], "subject": subject, "html": html}
    if reply_to:
        body["reply_to"] = reply_to
    try:
        resp = requests.post(url, headers={"Authorization": f"Bearer {key}"}, json=body, timeout=10)
        if not resp.ok:
            log.warning("Mail API answered %s: %s", resp.status_code, resp.text[:200])
        return resp.ok
    except Exception:
        log.exception("Could not send email")
        return False


@app.before_request
def need_database():
    if request.endpoint == "static":
        return None
    if not ensure_db():
        return render_template("setup.html", site_name=SITE_NAME, error=_db_error,
                               has_url=bool(os.environ.get("DATABASE_URL"))), (200 if request.method == "GET" else 503)
    return None


@app.get("/")
def index():
    return render_template("index.html", site_name=SITE_NAME, sent=request.args.get("sent") == "1", error=None, form={})


@app.post("/contact")
def contact():
    # Hidden field that only bots fill in. Pretend it worked.
    if request.form.get("website"):
        return render_template("index.html", site_name=SITE_NAME, sent=True, error=None, form={})
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    message = request.form.get("message", "").strip()
    form = {"name": name, "email": email, "message": message}
    if not name or "@" not in email or not message or len(name) > 200 or len(email) > 254 or len(message) > 5000:
        return render_template("index.html", site_name=SITE_NAME, sent=False,
                               error="Please fill in your name, a valid email and a message.", form=form), 400
    with psycopg.connect(os.environ["DATABASE_URL"], connect_timeout=10) as conn:
        conn.execute("INSERT INTO messages (name, email, message) VALUES (%s, %s, %s)", (name, email, message))
    owner = os.environ.get("OWNER_EMAIL")
    if owner:
        send_mail(
            owner,
            f"New message from {name}",
            f"<p><strong>{escape(name)}</strong> ({escape(email)}) wrote:</p>"
            f"<p>{escape(message).replace(chr(10), '<br>')}</p>",
            reply_to=email,
        )
    else:
        log.info("OWNER_EMAIL is not set; message saved but not emailed")
    return render_template("index.html", site_name=SITE_NAME, sent=True, error=None, form={})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

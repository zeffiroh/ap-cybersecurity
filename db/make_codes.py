#!/usr/bin/env python3
"""Make one-use unlock codes, store them in the Neon database and email them.

    python db/make_codes.py [count]

Run by .github/workflows/codes.yml every month. Reads the environment:
    DATABASE_URL    Neon connection string (owner, with password)
    SMTP_USER       Gmail address that sends the mail
    SMTP_PASSWORD   that account's app password
    MAIL_TO         where the codes go

The email also says how much has come in, from the payments db/sync_razorpay.py copies.
The repository is public and so are workflow logs: the codes are never printed.
If the mail can't be sent, the new codes are deleted again so no unknown codes stay valid.
"""
import csv
import io
import os
import secrets
import smtplib
import sys
from datetime import date
from email.message import EmailMessage

import psycopg

COURSE = "AP Cybersecurity"
PREFIX = "CYBER"                                   # tells this course's codes from other courses'
ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"   # no 0/O, 1/I: easy to read off a card


def code():
    part = lambda: "".join(secrets.choice(ALPHABET) for _ in range(4))
    return f"{PREFIX}-{part()}-{part()}-{part()}"


def rupees(paise):
    return f"Rs {paise / 100:,.2f}"


def earnings(db):
    """Two lines on money in (net of fees and refunds), from the payments the ledger sync copied."""
    total, n, month = db.execute(
        "select coalesce(sum(amount - amount_refunded - fee), 0), count(*), "
        "coalesce(sum(amount - amount_refunded - fee) filter (where created_at >= date_trunc('month', now() "
        "- interval '1 month') and created_at < date_trunc('month', now())), 0) "
        "from payments where status in ('captured', 'refunded')").fetchone()
    return f"Earned so far: {rupees(total)} from {n} payments (after fees and refunds).\nLast month: {rupees(month)}.\n"


def mail(codes, note, money):
    msg = EmailMessage()
    msg["Subject"] = f"{COURSE} unlock codes · {note}"
    msg["From"] = os.environ["SMTP_USER"]
    msg["To"] = os.environ["MAIL_TO"]
    msg.set_content(
        f"{len(codes)} new {COURSE} unlock codes ({note}). Each unlocks the full course for one account, once.\n"
        "Redeem at https://zeffiroh.github.io/ap-cybersecurity/unlock/\n\n" + "\n".join(codes) + "\n\n" + money)
    sheet = io.StringIO()
    csv.writer(sheet).writerows([["code", "course", "batch"]] + [[c, COURSE, note] for c in codes])
    msg.add_attachment(sheet.getvalue().encode(), maintype="text", subtype="csv",
                       filename=f"{PREFIX.lower()}-codes-{note}.csv")
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
        s.login(os.environ["SMTP_USER"], os.environ["SMTP_PASSWORD"])
        s.send_message(msg)


def main():
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    if not 1 <= count <= 500:
        sys.exit("count must be 1 to 500")
    note = date.today().strftime("%Y-%m")
    codes = [code() for _ in range(count)]
    with psycopg.connect(os.environ["DATABASE_URL"]) as db:
        db.cursor().executemany("insert into unlock_codes (code, uses_left, note) values (%s, 1, %s)",
                                [(c, f"monthly {note}") for c in codes])
        money = earnings(db)
    try:
        mail(codes, note, money)
    except Exception:
        with psycopg.connect(os.environ["DATABASE_URL"]) as db:
            db.execute("delete from unlock_codes where code = any(%s)", (codes,))
        raise
    print(f"{count} codes stored and mailed (batch {note}).")


if __name__ == "__main__":
    main()

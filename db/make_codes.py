#!/usr/bin/env python3
import csv
import io
import os
import secrets
import smtplib
import sys
from datetime import date
from email.message import EmailMessage

import psycopg

COURSE = "Aayat-AP-Prep"
PREFIX = "CYBER"
ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"


def code():
    part = lambda: "".join(secrets.choice(ALPHABET) for _ in range(4))
    return f"{PREFIX}-{part()}-{part()}-{part()}"


def money(minor, currency):
    return f"{'Rs' if currency == 'INR' else currency} {minor / 100:,.2f}"


def earnings(db):
    rows = db.execute(
        "select currency, coalesce(sum(amount - amount_refunded - fee), 0), count(*), "
        "coalesce(sum(amount - amount_refunded - fee) filter (where created_at >= date_trunc('month', now() "
        "- interval '1 month') and created_at < date_trunc('month', now())), 0) "
        "from payments where status in ('captured', 'refunded') group by currency "
        "order by currency <> 'INR', currency").fetchall() or [("INR", 0, 0, 0)]
    total = " + ".join(money(t, c) for c, t, _, _ in rows)
    month = " + ".join(money(m, c) for c, _, _, m in rows)
    n = sum(r[2] for r in rows)
    return f"Earned so far: {total} from {n} payments (after fees and refunds).\nLast month: {month}.\n"


def mail(codes, note, money):
    msg = EmailMessage()
    msg["Subject"] = f"{COURSE} unlock codes · {note}"
    msg["From"] = os.environ["SMTP_USER"]
    msg["To"] = os.environ["MAIL_TO"]
    msg.set_content(
        f"{len(codes)} new {COURSE} unlock codes ({note}). Each unlocks the full course for one account, once.\n"
        "Redeem at https://zeffiroh.github.io/ap-cybersecurity/store.html#redeem\n\n" + "\n".join(codes) + "\n\n" + money)
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

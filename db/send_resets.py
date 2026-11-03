#!/usr/bin/env python3
import os
import smtplib
from email.message import EmailMessage

import psycopg

COURSE = "Aayat-AP-Prep"
SITE = "https://zeffiroh.github.io/ap-cybersecurity/"


def message(email, code):
    msg = EmailMessage()
    msg["Subject"] = f"{COURSE}: your password reset code is {code}"
    msg["From"] = f"{COURSE} <{os.environ['SMTP_USER']}>"
    msg["To"] = email
    msg.set_content(
        f"Your {COURSE} password reset code is:\n\n    {code}\n\n"
        f"Enter it on the course site with a new password. The code works for 30 minutes.\n{SITE}\n\n"
        "If you didn't ask to reset your password, you can ignore this email; your password hasn't changed.\n")
    return msg


def main():
    if not os.environ.get("SMTP_PASSWORD"):
        print("no SMTP_PASSWORD; reset emails not sent")
        return
    with psycopg.connect(os.environ["DATABASE_URL"]) as db:
        due = db.execute("select email, code from reset_codes "
                         "where sent_at is null and expires_at > now() order by created_at").fetchall()
        if not due:
            print("no reset codes to send")
            return
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
            s.login(os.environ["SMTP_USER"], os.environ["SMTP_PASSWORD"])
            for email, code in due:
                s.send_message(message(email, code))
                db.execute("update reset_codes set sent_at = now() where email = %s and code = %s", (email, code))
                db.commit()
    print(f"sent {len(due)} reset code(s)")


if __name__ == "__main__":
    main()

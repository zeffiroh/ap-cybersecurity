#!/usr/bin/env python3
import os
import smtplib
from email.message import EmailMessage

import psycopg

COURSE = "Aayat-AP-Prep"
SITE = "https://zeffiroh.github.io/ap-cybersecurity/"


def message(to, title, note, free):
    msg = EmailMessage()
    msg["Subject"] = f"{COURSE}: new video lecture, {title}"
    msg["From"] = f"{COURSE} <{os.environ['SMTP_USER']}>"
    msg["To"] = to
    msg.set_content(
        f"A new video lecture is up: {title}\n\n" + (f"{note}\n\n" if note else "")
        + f"Watch it here (sign in first): {SITE}videos.html\n\n"
        + ("" if free else "Video lectures are part of the video pass.\n\n")
        + "You get this email because you're a student on the course.\n")
    return msg


def recipients(db, group_id, free):
    rows = db.execute(
        "select distinct a.email from accounts a "
        "where a.email not in (select email from teacher_emails) "
        "and (%s::bigint is null or a.email in (select email from group_members where group_id = %s::bigint)) "
        "and (%s or a.email in (select email from video_access where not revoked))",
        (group_id, group_id, free)).fetchall()
    return [r[0] for r in rows]


def main():
    if not os.environ.get("SMTP_PASSWORD"):
        print("no SMTP_PASSWORD; video notices not sent")
        return
    with psycopg.connect(os.environ["DATABASE_URL"]) as db:
        due = db.execute("select id, title, note, free, group_id from videos "
                         "where email_students and emailed_at is null order by created_at").fetchall()
        if not due:
            print("no video notices to send")
            return
        sent = 0
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
            s.login(os.environ["SMTP_USER"], os.environ["SMTP_PASSWORD"])
            for vid, title, note, free, group_id in due:
                for to in recipients(db, group_id, free):
                    s.send_message(message(to, title, note, free))
                    sent += 1
                db.execute("update videos set emailed_at = now() where id = %s", (vid,))
                db.commit()
    print(f"sent {sent} video notice(s)")


if __name__ == "__main__":
    main()

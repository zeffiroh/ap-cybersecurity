#!/usr/bin/env python3
import os
import smtplib
from email.message import EmailMessage
from urllib.parse import quote

import psycopg

COURSE = "Aayat-AP-Prep"
SITE = "https://zeffiroh.github.io/ap-cybersecurity/"
FOOT = ("\nYou get this email because you're a student on the course. "
        f"Turn these emails off on the Store page: {SITE}store.html\n")
OK = "not exists (select 1 from accounts acc where acc.email = {col} and acc.no_email)"


def message(to, subject, body, foot=FOOT):
    msg = EmailMessage()
    msg["Subject"] = f"{COURSE}: {subject}"
    msg["From"] = f"{COURSE} <{os.environ.get('SMTP_USER', 'noreply@example.com')}>"
    msg["To"] = to
    msg.set_content(body + foot)
    return msg


def when(t):
    return t.strftime("%a %d %b, %H:%M UTC")


def plural(n):
    return f"{n} ticket" + ("" if n == 1 else "s")


def videos(db):
    out = []
    for vid, title, note, free, group_id in db.execute(
            "select id, title, note, free, group_id from videos where email_students and emailed_at is null order by created_at").fetchall():
        rows = db.execute(
            "select distinct a.email from accounts a where a.email not in (select email from teacher_emails) and not a.no_email "
            "and (%s::bigint is null or a.email in (select email from group_members where group_id = %s::bigint)) "
            "and (%s or a.email in (select email from labs_access where not revoked))",
            (group_id, group_id, free)).fetchall()
        for (to,) in rows:
            out.append(message(to, f"new video lesson, {title}",
                               f"A new video lesson is up: {title}\n\n" + (f"{note}\n\n" if note else "")
                               + f"Watch it here (sign in first): {SITE}videos.html\n"
                               + ("" if free else "Lesson videos come with Labs.\n")))
        out.append(("update videos set emailed_at = now() where id = %s", (vid,)))
    return out


def tickets(db):
    out = []
    for lid, to, n, reason in db.execute(
            "select id, email, delta, reason from ticket_ledger where notified_at is null and delta > 0 "
            "and reason in ('razorpay', 'gumroad', 'code', 'gift') and " + OK.format(col="ticket_ledger.email") + " order by id").fetchall():
        bal = db.execute("select coalesce(sum(delta), 0) from ticket_ledger where email = %s", (to,)).fetchone()[0]
        how = {"razorpay": "Thanks for your purchase.", "gumroad": "Thanks for your purchase.", "code": "Your code worked.",
               "gift": "Your teacher sent them."}[reason]
        out.append(message(to, f"{plural(n)} added",
                           f"{how} {plural(n)} were added to your account. You now have {plural(bal)}.\n\n"
                           f"Book a class: {SITE}community.html#lectures\nUnlock a seminar: {SITE}seminars.html\n"))
        out.append(("update ticket_ledger set notified_at = now() where id = %s", (lid,)))
    db.execute("update ticket_ledger set notified_at = now() where notified_at is null and (delta <= 0 "
               "or reason not in ('razorpay', 'gumroad', 'code', 'gift') or not " + OK.format(col="ticket_ledger.email") + ")")
    return out


def seminars(db):
    out = []
    for sid, to, title in db.execute(
            "select a.seminar_id, a.email, s.title from seminar_access a join seminars s on s.id = a.seminar_id "
            "where a.notified_at is null and " + OK.format(col="a.email")).fetchall():
        out.append(message(to, f"seminar unlocked, {title}",
                           f"\"{title}\" is now yours to watch, as often as you like.\n\nWatch it: {SITE}seminars.html?id={sid}\n"
                           "Watch at least 90% of it to get a certificate.\n"))
        out.append(("update seminar_access set notified_at = now() where seminar_id = %s and email = %s", (sid, to)))
    for sub, to, until in db.execute(
            "select id, email, until from seminar_subs where notified_at is null and not revoked and " + OK.format(col="seminar_subs.email")).fetchall():
        out.append(message(to, "your seminars subscription is on",
                           f"You can watch every seminar, including new ones, until {until.strftime('%d %b %Y')}.\n\n"
                           f"Start here: {SITE}seminars.html\n"))
        out.append(("update seminar_subs set notified_at = now() where id = %s", (sub,)))
    db.execute("update seminar_access set notified_at = now() where notified_at is null and not " + OK.format(col="seminar_access.email"))
    db.execute("update seminar_subs set notified_at = now() where notified_at is null and (revoked or not " + OK.format(col="seminar_subs.email") + ")")
    return out


def classes(db):
    out = []
    for col, lo, hi, label in (("reminded_24", "75 minutes", "24 hours", "tomorrow"), ("reminded_1", "0 minutes", "75 minutes", "soon")):
        rows = db.execute(
            f"select c.id, c.title, c.starts_at, c.minutes, s.email from live_classes c join class_seats s on s.class_id = c.id "
            f"where c.status <> 'cancelled' and s.{col} is null and _seat_ok(c, s.email) "
            f"and c.starts_at > now() + interval '{lo}' and c.starts_at <= now() + interval '{hi}' "
            "and " + OK.format(col="s.email")).fetchall()
        for cid, title, starts, minutes, to in rows:
            out.append(message(to, f"class {label}: {title}",
                               f"Reminder: \"{title}\" starts {when(starts)} and runs {minutes} minutes.\n\n"
                               f"Join from the class page when it starts: {SITE}community.html\n"
                               "Can't make it? Cancel at least 2 hours before the start to get your tickets back.\n"))
            out.append((f"update class_seats set {col} = now() where class_id = %s and email = %s", (cid, to)))
    return out


def handins(db):
    out = []
    teachers = [t for (t,) in db.execute("select email from teacher_emails").fetchall()] or [t for t in [os.environ.get("MAIL_TO")] if t]
    for hid, who, title, note in db.execute(
            "select id, email, title, note from notebook_handins where status = 'new' and teacher_notified_at is null order by handed_at").fetchall():
        for to in teachers:
            out.append(message(to, "new hand-in",
                               f"{who} handed in: {title}\n\n" + (f"Their message: {note}\n\n" if note else "")
                               + f"Read it and reply: {SITE}teacher/handins.html\n", foot=""))
        out.append(("update notebook_handins set teacher_notified_at = now() where id = %s", (hid,)))
    for hid, to, ref, title, feedback in db.execute(
            "select id, email, ref, title, feedback from notebook_handins where status = 'replied' and student_notified_at is null and "
            + OK.format(col="notebook_handins.email") + " order by replied_at").fetchall():
        out.append(message(to, "your teacher replied",
                           f"Your teacher replied about {title}:\n\n{feedback}\n\nOpen your work: {SITE}notebook.html?ref={quote(ref)}\n"))
        out.append(("update notebook_handins set student_notified_at = now() where id = %s", (hid,)))
    return out


def main():
    dry = bool(os.environ.get("AAYAT_DRY_RUN"))
    if not dry and not os.environ.get("SMTP_PASSWORD"):
        print("no SMTP_PASSWORD; notices not sent")
        return
    with psycopg.connect(os.environ["DATABASE_URL"]) as db:
        sent = 0
        smtp = None
        try:
            for name, step in (("videos", videos), ("tickets", tickets), ("seminars", seminars), ("classes", classes), ("handins", handins)):
                items = step(db)
                for item in items:
                    if isinstance(item, tuple):
                        db.execute(*item)
                        continue
                    if dry:
                        print("---", item["To"], "|", item["Subject"])
                        print(item.get_content().strip())
                    else:
                        if smtp is None:
                            smtp = smtplib.SMTP_SSL("smtp.gmail.com", 465)
                            smtp.login(os.environ["SMTP_USER"], os.environ["SMTP_PASSWORD"])
                        smtp.send_message(item)
                    sent += 1
                db.commit()
        finally:
            if smtp is not None:
                smtp.quit()
    print(f"sent {sent} notice(s)")


if __name__ == "__main__":
    main()

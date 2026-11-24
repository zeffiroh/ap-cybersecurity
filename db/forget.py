#!/usr/bin/env python3
USAGE = """Delete one learner's data (the privacy notice promises this within 30 days of a request).

    python db/forget.py someone@example.com          show what would be deleted, change nothing
    python db/forget.py someone@example.com --yes    delete it

Kept, because tax and GST law needs them: payments, the ticket ledger, and the access rows that belong to a payment
(switched off, so the payment sync can't hand the access back). Forum threads that other people replied to stay,
with the learner's name and words removed.
The database comes from DATABASE_URL, or NEON_DATABASE_URL in .env.
"""
import sys
from datetime import date

import psycopg

DELETE = ["submissions", "engine_sessions", "activity", "accounts", "sessions", "reset_codes", "teacher_emails",
          "group_members", "class_requests", "class_attendance", "breakout_teams", "shared_updates", "shared_presence",
          "notebooks", "ctf_solves", "ctf_attempts", "seminar_access", "seminar_progress", "certificates",
          "notebook_handins", "forum_posts"]
PAID = ["unlocks", "labs_access", "seminar_subs", "video_access", "class_seats"]
KEEP = ["payments", "ticket_ledger"]
SPECIAL = ["forum_threads", "shared_notebooks"]
REMOVED = "[removed at the author's request]"


def has_column(db, table, col):
    return db.execute("select 1 from information_schema.columns where table_schema = 'public' and table_name = %s and column_name = %s",
                      (table, col)).fetchone() is not None


def plan(db, email):
    e = email.strip().lower()
    rows = []
    for t in DELETE:
        rows.append(("delete", t, db.execute(f"select count(*) from {t} where lower(email) = %s", (e,)).fetchone()[0]))
    for t in PAID:
        paid = db.execute(f"select count(*) from {t} x where lower(x.email) = %s and x.ref <> '' and exists (select 1 from payments p where p.id = x.ref)", (e,)).fetchone()[0]
        total = db.execute(f"select count(*) from {t} where lower(email) = %s", (e,)).fetchone()[0]
        rows.append(("delete", t, total - paid))
        if paid:
            rows.append(("keep, access off" if has_column(db, t, "revoked") else "keep", t, paid))
    alone = db.execute("""select count(*) from forum_threads t where lower(t.email) = %s and not exists
                          (select 1 from forum_posts p where p.thread_id = t.id and lower(p.email) <> %s)""", (e, e)).fetchone()[0]
    shared = db.execute("select count(*) from forum_threads where lower(email) = %s", (e,)).fetchone()[0] - alone
    rows.append(("delete", "forum_threads", alone))
    rows.append(("blank name and words", "forum_threads", shared))
    rows.append(("blank name", "shared_notebooks", db.execute("select count(*) from shared_notebooks where lower(updated_by) = %s", (e,)).fetchone()[0]))
    for t in KEEP:
        rows.append(("keep", t, db.execute(f"select count(*) from {t} where lower(email) = %s", (e,)).fetchone()[0]))
    return rows


def forget(db, email):
    e = email.strip().lower()
    db.execute("""delete from forum_threads t where lower(t.email) = %s and not exists
                  (select 1 from forum_posts p where p.thread_id = t.id and lower(p.email) <> %s)""", (e, e))
    for t in DELETE:
        db.execute(f"delete from {t} where lower(email) = %s", (e,))
    for t in PAID:
        db.execute(f"delete from {t} x where lower(x.email) = %s and not (x.ref <> '' and exists (select 1 from payments p where p.id = x.ref))", (e,))
        if has_column(db, t, "revoked"):
            db.execute(f"update {t} set revoked = true where lower(email) = %s", (e,))
    db.execute("update forum_threads set email = '', title = %s, body = '', deleted = true where lower(email) = %s", (REMOVED, e))
    db.execute("update shared_notebooks set updated_by = '' where lower(updated_by) = %s", (e,))


def main(argv):
    args = [a for a in argv if a != "--yes"]
    if len(args) != 1 or "@" not in args[0]:
        sys.exit(USAGE)
    email, go = args[0], "--yes" in argv
    from sql import url
    with psycopg.connect(url()) as db:
        rows = plan(db, email)
        print(f"{email}:")
        for what, table, n in rows:
            if n:
                print(f"  {what:<22} {n:>5}  {table}")
        if not any(n for what, _, n in rows if what != "keep"):
            print("  nothing to delete")
            return
        if not go:
            print("\nNothing changed. To delete it, run the same command with --yes at the end.")
            return
        forget(db, email)
        db.commit()
    print(f"\nDeleted on {date.today():%d %b %Y}. Reply to the learner that it's done. Their data also leaves the encrypted weekly")
    print("backups as those expire (90 days). Work saved only in their own browser is on their computer, not ours.")


if __name__ == "__main__":
    main(sys.argv[1:])

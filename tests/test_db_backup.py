import os
import shutil
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "db"))
sys.path.insert(0, str(ROOT / "tests"))

from test_schema_pg import BIN, free_port

try:
    import psycopg
    import backup as B
    import forget as F
except ImportError:
    psycopg = None

ME = "asha@example.com"
OTHER = "ravi@example.com"
SEED = f"""
insert into accounts (email, pass_hash) values ('{ME}', 'x'), ('{OTHER}', 'y');
insert into payments (id, status, amount, email, created_at) values ('pay_1', 'captured', 999900, '{ME}', now());
insert into unlocks (email, via, ref) values ('{ME}', 'razorpay', 'pay_1'), ('{ME}', 'code', 'CYBER-AAAA'), ('{OTHER}', 'code', 'CYBER-BBBB');
insert into labs_access (email, via, ref) values ('{ME}', 'labs_page', 'pay_1');
insert into ticket_ledger (email, delta, reason, ref) values ('{ME}', 5, 'tickets_page', 'pay:pay_1');
insert into submissions (email, topic_id, kind, item_id, response) values ('{ME}', '1.1', 'quiz', 'q1', 'it''s a phish'), ('{OTHER}', '1.1', 'quiz', 'q1', 'b');
insert into notebooks (email, ref, data) values ('{ME}', 'rb-x', '{{"cells": ["line one\\nline two\\ttab"]}}');
insert into forum_threads (space, email, title, body) values ('general', '{ME}', 'Only mine', 'alone'), ('general', '{ME}', 'Asked by me', 'my words');
insert into forum_posts (thread_id, email, body) select id, '{ME}', 'my reply' from forum_threads where title = 'Only mine';
insert into forum_posts (thread_id, email, body) select id, '{OTHER}', 'ravi answers' from forum_threads where title = 'Asked by me';
insert into shared_notebooks (space, updated_by) values ('class-a', '{ME}');
insert into seminars (title) values ('Seminar F');
insert into certificates (id, seminar_id, email, name, title) select 'C-1', id, '{ME}', 'Asha', 'Seminar F' from seminars;
"""


@unittest.skipUnless(BIN and psycopg, "PostgreSQL, psycopg or cryptography isn't installed")
class BackupAndForget(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp(prefix="aayat-bk-")
        data, cls.port = Path(cls.tmp) / "data", free_port()
        exe = lambda n: str(BIN / (n + (".exe" if os.name == "nt" else "")))
        subprocess.run([exe("initdb"), "-D", str(data), "-U", "postgres", "-A", "trust", "-E", "UTF8"], check=True, capture_output=True)
        cls.server = subprocess.Popen([exe("postgres"), "-D", str(data), "-p", str(cls.port), "-k", cls.tmp if os.name != "nt" else ""],
                                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for _ in range(60):
            if subprocess.run([exe("pg_isready"), "-h", "127.0.0.1", "-p", str(cls.port)], capture_output=True).returncode == 0:
                break
            time.sleep(0.5)
        with psycopg.connect(cls.url("postgres"), autocommit=True) as db:
            db.execute("create role anonymous; create role authenticated")
            for name in ("live", "spare", "forget"):
                db.execute(f"create database {name}")
        for name in ("live", "forget"):
            with psycopg.connect(cls.url(name), autocommit=True) as db:
                db.execute("create extension if not exists pgcrypto")
                db.execute((ROOT / "db" / "schema.sql").read_text(encoding="utf-8"))
                db.execute(SEED)
        with psycopg.connect(cls.url("spare"), autocommit=True) as db:
            db.execute("create extension if not exists pgcrypto")

    @classmethod
    def tearDownClass(cls):
        cls.server.terminate()
        cls.server.wait(timeout=30)
        shutil.rmtree(cls.tmp, ignore_errors=True)

    @classmethod
    def url(cls, name):
        return f"postgresql://postgres@127.0.0.1:{cls.port}/{name}"

    def rows(self, name, q):
        with psycopg.connect(self.url(name)) as db:
            return db.execute(q).fetchall()

    def test_backup_is_encrypted_and_restores(self):
        raw = B.dump(self.url("live"))
        blob = B.seal(raw, "correct horse")
        self.assertNotIn(ME.encode(), blob)
        self.assertNotIn(b"Only mine", blob)
        with self.assertRaises(SystemExit):
            B.load(blob, "wrong")
        data = B.load(blob, "correct horse")
        self.assertIn("payments", B.summary(data))
        B.restore(data, self.url("spare"))
        for q in ("select email, response from submissions order by id", "select email, ref, data::text from notebooks",
                  "select title, body from forum_threads order by id", "select id, email, name from certificates",
                  "select email, via, ref, revoked from unlocks order by id"):
            self.assertEqual(self.rows("spare", q), self.rows("live", q), q)
        with psycopg.connect(self.url("spare")) as db:
            db.execute(f"insert into unlocks (email) values ('new@example.com')")
            db.execute(f"insert into submissions (email, topic_id, kind, item_id) values ('new@example.com', '1.1', 'quiz', 'q2')")
            db.commit()
        B.restore(data, self.url("spare"))
        self.assertEqual(self.rows("spare", "select count(*) from unlocks")[0][0], 3)

    def test_forget_plan_covers_every_table_with_an_email(self):
        found = {r[0] for r in self.rows("live", """select table_name from information_schema.columns where table_schema = 'public'
                                                     and (column_name = 'email' or column_name = 'updated_by')""")}
        planned = set(F.DELETE) | set(F.PAID) | set(F.KEEP) | set(F.SPECIAL)
        self.assertEqual(found - planned, set(), "a table with an email column isn't in db/forget.py")
        self.assertEqual(planned - found, set())

    def test_forget_deletes_the_learner_and_keeps_tax_records(self):
        with psycopg.connect(self.url("forget")) as db:
            before = dict(((w, t), n) for w, t, n in F.plan(db, ME))
            self.assertEqual(before[("delete", "accounts")], 1)
            self.assertEqual(before[("keep, access off", "unlocks")], 1)
            F.forget(db, ME.upper())
            db.commit()
        one = lambda q: self.rows("forget", q)
        for t in ("accounts", "submissions", "notebooks", "certificates", "forum_posts"):
            self.assertEqual(one(f"select count(*) from {t} where email = '{ME}'")[0][0], 0, t)
        self.assertEqual(one(f"select ref, revoked from unlocks where email = '{ME}'"), [("pay_1", True)])
        self.assertEqual(one(f"select revoked from labs_access where email = '{ME}'"), [(True,)])
        self.assertEqual(one(f"select count(*) from payments where email = '{ME}'")[0][0], 1)
        self.assertEqual(one(f"select count(*) from ticket_ledger where email = '{ME}'")[0][0], 1)
        self.assertEqual(one("select email, title, body, deleted from forum_threads"), [("", F.REMOVED, "", True)])
        self.assertEqual(one("select email, body from forum_posts"), [(OTHER, "ravi answers")])
        self.assertEqual(one("select updated_by from shared_notebooks"), [("",)])
        self.assertEqual(one(f"select count(*) from accounts where email = '{OTHER}'")[0][0], 1)
        with psycopg.connect(self.url("forget")) as db:
            self.assertFalse(any(n for w, _, n in F.plan(db, ME) if not w.startswith("keep")))


if __name__ == "__main__":
    unittest.main()

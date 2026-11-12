import json
import os
import shutil
import socket
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "db" / "schema.sql"


def pg_bin():
    for base in [os.environ.get("PG_BIN", "")] + sorted(Path("C:/Program Files/PostgreSQL").glob("*/bin"), reverse=True) + [Path("/usr/lib/postgresql")]:
        if base and (Path(base) / ("initdb.exe" if os.name == "nt" else "initdb")).exists():
            return Path(base)
    found = shutil.which("initdb")
    return Path(found).parent if found else None


BIN = pg_bin()


def free_port():
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    p = s.getsockname()[1]
    s.close()
    return p


@unittest.skipUnless(BIN, "PostgreSQL isn't installed")
class Schema(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp(prefix="aayat-pg-")
        cls.data = Path(cls.tmp) / "data"
        cls.port = free_port()
        exe = lambda n: str(BIN / (n + (".exe" if os.name == "nt" else "")))
        cls.exe = exe
        subprocess.run([exe("initdb"), "-D", str(cls.data), "-U", "postgres", "-A", "trust", "-E", "UTF8"], check=True, capture_output=True)
        cls.server = subprocess.Popen([exe("postgres"), "-D", str(cls.data), "-p", str(cls.port), "-k", cls.tmp if os.name != "nt" else ""],
                                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for _ in range(60):
            if subprocess.run([exe("pg_isready"), "-h", "127.0.0.1", "-p", str(cls.port)], capture_output=True).returncode == 0:
                break
            time.sleep(0.5)
        cls.sql("create role anonymous; create role authenticated; create extension if not exists pgcrypto;")
        for _ in range(2):
            cls.sql(SCHEMA.read_text(encoding="utf-8"), stop=True)
        cls.sql("insert into teacher_keys (hash, note) values (_sha('k'), 'test');")

    @classmethod
    def tearDownClass(cls):
        cls.server.terminate()
        cls.server.wait(timeout=30)
        shutil.rmtree(cls.tmp, ignore_errors=True)

    @classmethod
    def sql(cls, text, stop=False, teacher=False):
        pre = "set request.headers = '{\"x-teacher-key\": \"k\"}';\n" if teacher else ""
        r = subprocess.run([cls.exe("psql"), "-h", "127.0.0.1", "-p", str(cls.port), "-U", "postgres", "-d", "postgres", "-qAt", "-v", "ON_ERROR_STOP=1" if stop else "ON_ERROR_STOP=0"],
                           input=pre + text, capture_output=True, text=True, encoding="utf-8")
        if stop and r.returncode != 0:
            raise AssertionError(r.stderr[-2000:])
        return r.stdout.strip(), r.stderr.strip()

    def one(self, q, teacher=False):
        out, err = self.sql(q, teacher=teacher)
        self.assertFalse("ERROR" in err, err)
        return out.splitlines()[-1] if out else ""

    def test_seminar_drafts_load_twice_and_stay_hidden(self):
        seed = (ROOT / "db" / "seminars.sql").read_text(encoding="utf-8")
        self.sql("delete from seminars where id between 1 and 13;", stop=True)
        self.sql(seed, stop=True)
        self.sql(seed, stop=True)
        self.assertEqual(self.one("select count(*) from seminars where id between 1 and 13;"), "13")
        self.assertEqual(self.one("select count(*) from seminars where title = 'Capstone B: a breach across teams' and tickets = 16 and not published;"), "1")
        self.assertEqual(self.one("select count(*) from seminars where title = 'Evidence, notes and handoffs' and tickets = 0;"), "1")
        self.assertNotIn("Capstone B", self.one("select api_seminars();"))
        self.assertIn("Capstone B", self.one("select api_teacher_seminars();", teacher=True))
        self.assertGreater(int(self.one("select nextval(pg_get_serial_sequence('seminars', 'id'));")), 13)

    def test_ticket_expiry_off_is_a_plain_sum(self):
        self.sql("delete from settings where key = 'ticket_expiry_days'; insert into ticket_ledger (email, delta, reason) values ('a@x.org', 5, 'gift'), ('a@x.org', -2, 'class');")
        self.assertEqual(self.one("select _tickets('a@x.org');"), "3")

    def test_ticket_expiry_spends_oldest_first(self):
        self.sql("insert into settings (key, value) values ('ticket_expiry_days', '30') on conflict (key) do update set value = excluded.value;"
                 "insert into ticket_ledger (email, delta, reason, created_at) values ('b@x.org', 4, 'old', now() - interval '40 days'), "
                 "('b@x.org', -3, 'class', now() - interval '35 days'), ('b@x.org', 5, 'new', now() - interval '5 days'), ('b@x.org', -2, 'class', now() - interval '1 day');")
        self.assertEqual(self.one("select _tickets('b@x.org');"), "3")
        lots = json.loads(self.one("select _ticket_lots('b@x.org');"))
        self.assertEqual([l["left"] for l in lots], [3])
        self.sql("delete from settings where key = 'ticket_expiry_days';")
        self.assertEqual(self.one("select _tickets('b@x.org');"), "4")

    def test_spend_respects_expiry(self):
        self.sql("insert into settings (key, value) values ('ticket_expiry_days', '10') on conflict (key) do update set value = excluded.value;"
                 "insert into ticket_ledger (email, delta, reason, created_at) values ('c@x.org', 3, 'old', now() - interval '20 days');")
        self.assertEqual(self.one("select _spend('c@x.org', 1, 'class', 'class:1');"), "f")
        self.sql("delete from settings where key = 'ticket_expiry_days';")
        self.assertEqual(self.one("select _spend('c@x.org', 1, 'class', 'class:1');"), "t")

    def test_handin_rubric_goes_to_the_gradebook(self):
        hid = self.one("insert into notebook_handins (email, ref, title) values ('s@x.org', 'rb-web01', 'Web01 runbook') returning id;")
        r = json.loads(self.one("select api_teacher_handin_grade('{\"id\": %s, \"feedback\": \"Good\", \"rubric\": [{\"c\": \"Evidence\", \"max\": 4, \"got\": 3}, {\"c\": \"Answers\", \"max\": 6, \"got\": 9}]}'::jsonb);" % hid, teacher=True))
        self.assertTrue(r["ok"])
        self.assertEqual((float(r["score"]), float(r["max"])), (9.0, 10.0))
        self.assertEqual(self.one("select points || '/' || max_points from submissions where email = 's@x.org' and kind = 'handin';"), "9/10")
        mine = json.loads(self.one("select api_teacher_handin(%s);" % hid, teacher=True))
        self.assertEqual(len(mine["item"]["rubric"]), 2)

    def test_teacher_only_functions_refuse_students(self):
        _, err = self.sql("select api_teacher_handin_grade('{\"id\": 1, \"rubric\": []}'::jsonb);")
        self.assertIn("teacher key required", err)
        _, err = self.sql("select api_teacher_checklist_set('{}'::jsonb);")
        self.assertIn("teacher key required", err)

    def test_checklist_and_rubric_library_round_trip(self):
        self.one("select api_teacher_checklist_set('{\"s1\": [\"unlisted\"]}'::jsonb);", teacher=True)
        self.assertEqual(json.loads(self.one("select api_teacher_checklist_get();", teacher=True)), {"s1": ["unlisted"]})
        self.one("select api_teacher_rubrics_set('{\"Runbook\": [{\"c\": \"Evidence\", \"max\": 4}]}'::jsonb);", teacher=True)
        self.assertIn("Runbook", json.loads(self.one("select api_teacher_rubrics_get();", teacher=True)))

    def test_certificate_carries_the_outline_and_domains(self):
        sid = json.loads(self.one("select api_teacher_save_seminar('{\"title\": \"Night shift\", \"minutes\": 90, \"domains\": [\"Security Operations\", \" \"], "
                                  "\"chapters\": [{\"t\": \"0:00\", \"title\": \"Handover\", \"d\": \"Security Operations\"}, {\"t\": \"45:00\", \"title\": \"Report\", \"d\": \"Incident Response\"}]}'::jsonb);", teacher=True))["id"]
        self.sql(f"insert into certificates (id, seminar_id, email, name, title, minutes) values ('AAP-TEST-0001', {sid}, 'z@x.org', 'Zed', 'Night shift', 90);")
        c = json.loads(self.one("select api_certificate('aap-test-0001');"))
        self.assertTrue(c["ok"])
        self.assertEqual(c["domains"], ["Security Operations"])
        self.assertEqual([x["d"] for x in c["chapters"]], ["Security Operations", "Incident Response"])

    def test_save_video_updates_the_email_flag(self):
        vid = json.loads(self.one("select api_teacher_save_video('{\"youtube\": \"dQw4w9WgXcQ\", \"title\": \"A video\", \"email\": false}'::jsonb);", teacher=True))["id"]
        self.one("select api_teacher_save_video('{\"id\": %s, \"youtube\": \"dQw4w9WgXcQ\", \"title\": \"A video\", \"email\": true}'::jsonb);" % vid, teacher=True)
        self.assertEqual(self.one("select email_students from videos where id = %s;" % vid), "t")


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3
"""Copy Razorpay payments into the database, and unlock the course for everyone who paid.

    python db/sync_razorpay.py          the last 60 days (everything, the first time)
    python db/sync_razorpay.py --all    everything since the account opened

Run every 5 minutes by .github/workflows/ledger.yml. A captured payment from the course's payment page
(PAGE_ID) unlocks the email typed in its EMAIL_FIELD; a full refund takes that unlock back. Re-reading 60
days picks up refunds and late captures. Keys come from RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET, or from
the CSV named by RAZORPAY_KEY_FILE (columns key_id, key_secret); the database as in db/sql.py.
The repository is public and so are workflow logs: nothing about the payments is printed.
"""
import base64
import csv
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

import psycopg
from psycopg.types.json import Jsonb

from sql import url

API = "https://api.razorpay.com/v1"
PAGE_ID = "pl_TtJ7iha8pa0yTa"                       # rzp.io/rzp/unlock-aap-cybersecurity
EMAIL_FIELD = "email_you_sign_in_to_the_course_with"
PRIVATE = re.compile(r"phone|contact|mobile", re.I)  # form fields never stored
EARLIEST = 946684800                                 # 2000-01-01, the oldest "from" Razorpay accepts
PAGE = 100
EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


def keys():
    if os.environ.get("RAZORPAY_KEY_ID"):
        return os.environ["RAZORPAY_KEY_ID"], os.environ["RAZORPAY_KEY_SECRET"]
    if os.environ.get("RAZORPAY_KEY_FILE"):
        with open(os.environ["RAZORPAY_KEY_FILE"], encoding="utf-8-sig", newline="") as f:
            row = next(csv.DictReader(f))
        return row["key_id"].strip(), row["key_secret"].strip()
    sys.exit("No Razorpay keys: set RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET, or RAZORPAY_KEY_FILE")


AUTH = "Basic " + base64.b64encode(":".join(keys()).encode()).decode()


def get(path, **query):
    req = urllib.request.Request(f"{API}/{path}?{urllib.parse.urlencode(query)}", headers={"Authorization": AUTH})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def payments(since):
    until, skip = int(time.time()), 0
    while True:
        items = get("payments", **{"from": since, "to": until, "count": PAGE, "skip": skip})["items"]
        yield from items
        if len(items) < PAGE:
            return
        skip += PAGE


def notes(p, orders):
    """The payment's form fields: on the payment, or on the order the payment page made for it."""
    n = p.get("notes") or {}
    n = dict(n) if isinstance(n, dict) else {}
    if EMAIL_FIELD not in n and p.get("order_id"):
        if p["order_id"] not in orders:
            o = get(f"orders/{p['order_id']}")
            on = o.get("notes") or {}
            orders[p["order_id"]] = dict(on, _page=PAGE_ID in json.dumps(o)) if isinstance(on, dict) else {}
        n = {**orders[p["order_id"]], **n}
    return n


def main():
    with psycopg.connect(url()) as db:
        empty = db.execute("select not exists (select 1 from payments where id <> '_sync')").fetchone()[0]
        since = EARLIEST if empty or "--all" in sys.argv else int(time.time()) - 60 * 86400
        orders, rows, unlocks = {}, [], []
        for p in payments(since):
            n = notes(p, orders)
            course = n.pop("_page", False) or EMAIL_FIELD in n or PAGE_ID in json.dumps(p)
            email = str(n.get(EMAIL_FIELD) or p.get("email") or "").strip().lower()[:200]
            kept = {k: str(v)[:500] for k, v in n.items() if not PRIVATE.search(k)}
            rows.append((p["id"], p["status"], p.get("amount") or 0, p.get("amount_refunded") or 0, p.get("fee") or 0,
                         p.get("tax") or 0, p.get("currency") or "INR", p.get("method") or "", email,
                         (p.get("description") or "")[:300], Jsonb(kept), p["created_at"]))
            if course and EMAIL_RE.match(email):
                paid = p["status"] in ("captured", "refunded") and (p.get("amount_refunded") or 0) < (p.get("amount") or 0)
                unlocks.append((email, p["id"], paid))
        db.cursor().executemany(
            """insert into payments (id, status, amount, amount_refunded, fee, tax, currency, method, email,
                                     description, notes, created_at)
               values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, to_timestamp(%s))
               on conflict (id) do update set
                 status = excluded.status, amount_refunded = excluded.amount_refunded, fee = excluded.fee,
                 tax = excluded.tax, method = excluded.method, email = excluded.email, notes = excluded.notes,
                 synced_at = now()""",
            rows)
        for email, ref, paid in unlocks:
            if paid:
                db.execute("insert into unlocks (email, via, ref) select %s, 'razorpay', %s "
                           "where not exists (select 1 from unlocks where via = 'razorpay' and ref = %s)",
                           (email, ref, ref))
            else:                                    # refunded in full, or not captured after all
                db.execute("update unlocks set revoked = true where via = 'razorpay' and ref = %s", (ref,))
        db.execute("insert into payments (id, status, created_at) values ('_sync', 'sync', now()) "
                   "on conflict (id) do update set synced_at = now()")   # when it last ran, even with no sales
    print("Razorpay sync done.")


if __name__ == "__main__":
    main()
